import boto3

def store_agent_arn_in_parameter_store(parameter_name, agent_arn, region='us-east-1'):
    """Store agent ARN in AWS Systems Manager Parameter Store"""
    ssm_client = boto3.client('ssm', region_name=region)
    
    try:
        response = ssm_client.put_parameter(
            Name=parameter_name,
            Value=agent_arn,
            Type='String',
            Overwrite=True,
            Description='Bedrock AgentCore Runtime ARN for mahen_tech_agent'
        )
        print(f"Successfully stored ARN in parameter: {parameter_name}")
        return True
    except Exception as e:
        print(f"Error storing parameter {parameter_name}: {e}")
        return False

if __name__ == "__main__":
    # Store the agent ARN
    agent_arn = "arn:aws:bedrock-agentcore:us-east-1:471727841202:runtime/mahen_hr_agent-TnJnXMCleG"
    parameter_name = "/agents/mahen_hr_agent/arn"
    
    store_agent_arn_in_parameter_store(parameter_name, agent_arn)