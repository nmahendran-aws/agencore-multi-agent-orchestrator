import boto3
import json

def get_agent_arn_from_parameter_store(parameter_name, region='us-east-1'):
    """Get agent ARN from AWS Systems Manager Parameter Store"""
    ssm_client = boto3.client('ssm', region_name=region)
    
    try:
        response = ssm_client.get_parameter(Name=parameter_name)
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error retrieving parameter {parameter_name}: {e}")
        return None

def invoke_agent_from_parameter_store(parameter_name, prompt, region='us-east-1'):
    """Invoke agent using ARN from parameter store"""
    # Get ARN from parameter store
    agent_runtime_arn = get_agent_arn_from_parameter_store(parameter_name, region)
    
    if not agent_runtime_arn:
        return "Failed to retrieve agent ARN from parameter store"
    
    # Invoke agent
    client = boto3.client('bedrock-agentcore', region_name=region)
    
    payload = {"prompt": prompt}
    
    response = client.invoke_agent_runtime(
        agentRuntimeArn=agent_runtime_arn,
        payload=json.dumps(payload)
    )
    
    return response['response'].read().decode('utf-8')

if __name__ == "__main__":
    # Example usage
    parameter_name = "/agents/mahen_orchestrator_agent_arn"  # Adjust parameter name as needed
    prompt = "Hello, tell me about my benefits, also tell me how to connect a bluetooth mouse to my mac?"
    
    response = invoke_agent_from_parameter_store(parameter_name, prompt)
    print("Agent Response:", response)