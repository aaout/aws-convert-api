# https://community.aws/content/2hW7srTWRb5idHjY4I8WP5fQFRf/build-a-tool-use-based-agent-loop-with-amazon-bedrock

import boto3
import json
import math
from pydantic import BaseModel


class ToolError(Exception):
    pass


def call_bedrock(message_list, tool_list):
    """bedrockに入力メッセージとツールを入力し、
    LLMからのレスポンスを返す関数

    Args:
        message_list (_type_): 入力メッセージ
        tool_list (_type_): ツール

    Returns:
        _type_: LLMからのレスポンス
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
    )

    return response


def get_tool_result(tool_use_block):
    """AgentがtoolUseした際のロジックを実装する関数
    予め用意していおいたtool_listの中から、呼び出されたtoolに応じて条件分岐

    Args:
        tool_use_block (_type_): _description_

    Raises:
        ToolError: _description_

    Returns:
        _type_: _description_
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
