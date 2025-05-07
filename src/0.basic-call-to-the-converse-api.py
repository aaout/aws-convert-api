# https://community.aws/content/2hHgVE7Lz6Jj1vFv39zSzzlCilG/getting-started-with-the-amazon-bedrock-converse-api

import boto3
import json

session = boto3.Session()
bedrock = session.client(service_name="bedrock-runtime", region_name="ap-northeast-3")

message_list = []

initial_message = {
    "role": "user",
    "content": [{"text": "How are you today?"}],
}

message_list.append(initial_message)

response = bedrock.converse(
    modelId="apac.anthropic.claude-3-5-sonnet-20241022-v2:0",
    messages=message_list,
    inferenceConfig={"maxTokens": 2000, "temperature": 0},
)

response_message = response["output"]["message"]
print(json.dumps(response_message, indent=4))
