# https://community.aws/content/2hHgVE7Lz6Jj1vFv39zSzzlCilG/getting-started-with-the-amazon-bedrock-converse-api

import boto3
import json
from pydantic import BaseModel


class ContentItem(BaseModel):
    text: str


class Message(BaseModel):
    role: str
    content: list[ContentItem]


session = boto3.Session()
bedrock = session.client(service_name="bedrock-runtime", region_name="ap-northeast-1")

message_list = []

initial_message = {
    "role": "user",
    "content": [{"text": "元気ですか?"}],
}

parsed_message = Message(**initial_message).model_dump()
print(json.dumps(parsed_message, indent=4, ensure_ascii=False))

message_list.append(parsed_message)

response = bedrock.converse(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages=message_list,
    inferenceConfig={"maxTokens": 2000, "temperature": 0},
)["output"]["message"]
parsed_response = Message(**response).model_dump()
print(json.dumps(parsed_response, indent=4, ensure_ascii=False))
