# Let's update the orchestrator agentcore exeuction role so it has permissions to invoke the required subagents
# the orchestrator also needs needs permissions to retrieve the sub agent arns from parameter store
import json
import boto3

orchestrator_role_name = "agentcore-orchestrator_agent-role" 

# retrieve the runtime arn from parameter store
ssm = boto3.client('ssm')
response = ssm.get_parameter(Name='/agents/mahen_tech_agent_arn')
tech_agent_arn = response['Parameter']['Value']
tech_agent_parameter_arn = response['Parameter']['ARN']

ssm = boto3.client('ssm')
response = ssm.get_parameter(Name='/agents/mahen_hr_agent/arn')
hr_agent_arn = response['Parameter']['Value']
hr_agent_parameter_arn = response['Parameter']['ARN']

def update_orchestrator_permissions(sub_agent_arns: list, sub_agent_parameter_arns: list, orchestrator_name: str):
    iam_client = boto3.client('iam')
    orchestrator_permissions = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock-agentcore:InvokeAgentRuntime"
                ],
                "Resource": [ sub_agent_arn + "/runtime-endpoint/DEFAULT" for sub_agent_arn in sub_agent_arns ] + [ sub_agent_arn for sub_agent_arn in sub_agent_arns ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ssm:GetParameter"
                ],
                "Resource": [sub_agent_parameter_arn for sub_agent_parameter_arn in sub_agent_parameter_arns]

            }]
    }
        
    rsp = iam_client.put_role_policy(
        RoleName=orchestrator_name,
        PolicyName="subagent_permissions-new",
        PolicyDocument=json.dumps(orchestrator_permissions)
    )
    return rsp

rsp = update_orchestrator_permissions([tech_agent_arn, hr_agent_arn], [tech_agent_parameter_arn, hr_agent_parameter_arn], orchestrator_role_name)
print(rsp)