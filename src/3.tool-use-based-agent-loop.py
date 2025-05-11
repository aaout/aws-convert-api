# https://community.aws/content/2hW7srTWRb5idHjY4I8WP5fQFRf/build-a-tool-use-based-agent-loop-with-amazon-bedrock

import boto3
import json
import math
from pydantic import BaseModel

from tools import tools
from prompt import system_prompt


class ToolError(Exception):
    pass


def call_bedrock(message_list, tool_list):
    """bedrockに入力メッセージとツールを入力し、
    LLMからのレスポンスを返す関数
    """
    session = boto3.Session()

    bedrock = session.client(
        service_name="bedrock-runtime", region_name="ap-northeast-1"
    )

    response = bedrock.converse(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=message_list,
        inferenceConfig={"maxTokens": 2000, "temperature": 0},
        toolConfig={"tools": tool_list},
        system=[{"text": system_prompt}],
    )

    return response


def get_tool_result(tool_use_block):
    """AgentがtoolUseした際のロジックを実装する関数
    予め用意していおいたtool_listの中から、呼び出されたtoolに応じて条件分岐
    """
    tool_use_name = tool_use_block["name"]

    print(f"Using tool {tool_use_name}")

    # Note: We're deliberately excluding tangent so something magical can happen
    if tool_use_name == "cosine":
        return math.cos(tool_use_block["input"]["x"])
    elif tool_use_name == "sine":
        return math.sin(tool_use_block["input"]["x"])
    elif tool_use_name == "divide_numbers":
        return tool_use_block["input"]["x"] / tool_use_block["input"]["y"]
    else:
        raise ToolError(f"Invalid function name: {tool_use_name}")


def handle_response(response_message):
    """Agentからのレスポンスを入力し, toolsを使用した場合はそれに応じたロジックを実行する
    response_message["content"]にはAgentからのレスポンスがリストとして格納されている
    レスポンスのkeyにtoolUseが含まれている場合は条件分岐でロジックを呼び出す
    toolを実行した結果はfollow_up_content_blocksに追加し, Messageとして返す
    """
    response_content_blocks = response_message["content"]

    follow_up_content_blocks = []

    for content_block in response_content_blocks:
        if "toolUse" in content_block:
            tool_use_block = content_block["toolUse"]

            try:
                tool_result_value = get_tool_result(tool_use_block)

                if tool_result_value is not None:
                    follow_up_content_blocks.append(
                        {
                            "toolResult": {
                                "toolUseId": tool_use_block["toolUseId"],
                                "content": [{"json": {"result": tool_result_value}}],
                            }
                        }
                    )

            except ToolError as e:
                follow_up_content_blocks.append(
                    {
                        "toolResult": {
                            "toolUseId": tool_use_block["toolUseId"],
                            "content": [{"text": repr(e)}],
                            "status": "error",
                        }
                    }
                )

    if len(follow_up_content_blocks) > 0:
        follow_up_message = {
            "role": "user",
            "content": follow_up_content_blocks,
        }

        return follow_up_message
    else:
        return None


def run_loop(prompt, tool_list):
    """ """
    MAX_LOOPS = 10
    loop_count = 0
    continue_loop = True

    message_list = [{"role": "user", "content": [{"text": prompt}]}]

    while continue_loop:
        response = call_bedrock(message_list, tool_list)

        response_message = response["output"]["message"]
        message_list.append(response_message)

        loop_count = loop_count + 1

        if loop_count >= MAX_LOOPS:
            print(f"Hit loop limit: {loop_count}")
            break

        follow_up_message = handle_response(response_message)

        # toolUseしたかどうかで条件分岐
        if follow_up_message is None:
            # 使用していない場合はloopを抜けてAgentの思考をストップ
            continue_loop = False
        else:
            # 使用した場合, toolUseの実行結果をmessage_listに追加し、
            # その結果を踏まえてAgentはもう一度レスポンス内容を思考する
            message_list.append(follow_up_message)

    return message_list


messages = run_loop("What is the tangent of 7?", tools)

print("\nMESSAGES:\n")
print(json.dumps(messages, indent=4, ensure_ascii=False))
