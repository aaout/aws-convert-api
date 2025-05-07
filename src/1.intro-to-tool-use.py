import boto3
import json
import math

session = boto3.Session()
bedrock = session.client(service_name="bedrock-runtime", region_name="ap-northeast-3")

tool_list = [
    {
        "toolSpec": {
            "name": "cosine",
            "description": "Calculate the cosine of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        }
                    },
                    "required": ["x"],
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "sum",
            "description": "Calculate the sum of all arguments.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x0": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x1": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x2": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x3": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x4": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x5": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x6": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x7": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x8": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                        "x9": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        },
                    },
                    "required": [
                        "x0",
                        "x1",
                        "x2",
                        "x3",
                        "x4",
                        "x5",
                        "x6",
                        "x7",
                        "x8",
                        "x9",
                    ],
                }
            },
        }
    },
]

message_list = []

initial_message = {
    "role": "user",
    # "content": [{"text": "What is the cosine of 7?"}],
    "content": [{"text": "Calculate the following addition: 1+2+3+4+5+6+7+8+9+10"}],
}

message_list.append(initial_message)
print(json.dumps(message_list, indent=4))

response = bedrock.converse(
    modelId="apac.anthropic.claude-3-5-sonnet-20241022-v2:0",
    messages=message_list,
    inferenceConfig={"maxTokens": 2000, "temperature": 0},
    toolConfig={"tools": tool_list},
    system=[{"text": "You must only do math by using a tool."}],
)

response_message = response["output"]["message"]
print(json.dumps(response_message, indent=4))
message_list.append(response_message)

response_content_blocks = response_message["content"]

for content_block in response_content_blocks:
    if "toolUse" in content_block:
        tool_use_block = content_block["toolUse"]
        tool_use_name = tool_use_block["name"]

        print(f"Using tool {tool_use_name}")

        if tool_use_name == "cosine":
            tool_result_value = math.cos(tool_use_block["input"]["x"])
            print(tool_result_value)

        if tool_use_name == "sum":
            tool_result_value = sum(
                [
                    tool_use_block["input"]["x0"],
                    tool_use_block["input"]["x1"],
                    tool_use_block["input"]["x2"],
                    tool_use_block["input"]["x3"],
                    tool_use_block["input"]["x4"],
                    tool_use_block["input"]["x5"],
                    tool_use_block["input"]["x6"],
                    tool_use_block["input"]["x7"],
                    tool_use_block["input"]["x8"],
                    tool_use_block["input"]["x9"],
                ]
            )
            print(tool_result_value)

    elif "text" in content_block:
        print(content_block["text"])
