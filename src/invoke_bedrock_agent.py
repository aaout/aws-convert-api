import uuid
import boto3
import streamlit as st

# Agentへの入力テキスト
input_text: str = "Bedrockで使用可能なモデルは？"

# Agentの定義
agent_id: str = "RRPLLJUQDN"
agent_alias_id: str = "IMZ1VTBRQD"
session_id: str = str(uuid.uuid1())  # 乱数

# Clientの定義
client = boto3.client("bedrock-agent-runtime", region_name="ap-northeast-1")

st.title("Bedrock Agent")
input_text = st.text_input("入力テキスト")
send_button = st.button("送信")


if send_button:
    result_area = st.empty()
    text = ""

    # Agentの実行
    response = client.invoke_agent(
        inputText=input_text,
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        enableTrace=False,
    )

    # Agent実行結果の取得
    event_stream = response["completion"]
    for event in event_stream:
        if "chunk" in event:
            text += event["chunk"]["bytes"].decode("utf-8")
            result_area.write(text)
