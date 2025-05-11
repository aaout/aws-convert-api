# https://community.aws/content/2hW7srTWRb5idHjY4I8WP5fQFRf/build-a-tool-use-based-agent-loop-with-amazon-bedrock

import boto3
import json
import math


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
