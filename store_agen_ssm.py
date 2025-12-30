mahen_tech_agent_arn = "arn:aws:bedrock-agentcore:us-east-1:471727841202:runtime/mahen_tech_agent-bgFBX1GVzl"

import boto3
import time

ssm = boto3.client('ssm')
ssm.put_parameter(
    Name=f'/agents/mahen_tech_agent_arn',
    Value=mahen_tech_agent_arn,
    Type='String',
    Overwrite=True
)