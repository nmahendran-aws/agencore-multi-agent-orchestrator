import boto3
import json

# Direct invoke using the deployed agent ARN
agent_runtime_arn = "arn:aws:bedrock-agentcore:us-east-1:471727841202:runtime/mahen_tech_agent-bgFBX1GVzl"

client = boto3.client('bedrock-agentcore', region_name='us-east-1')

payload = {
    "prompt": "Hello, can you help me with a technical question?"
}

response = client.invoke_agent_runtime(
    agentRuntimeArn=agent_runtime_arn,
    payload=json.dumps(payload)
)

# Read the streaming response
response_body = response['response'].read().decode('utf-8')
print("Agent Response:", response_body)