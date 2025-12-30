
import argparse
import json
import boto3
import logging

from strands import Agent, tool
from strands_tools import calculator 
from strands.models import BedrockModel

from bedrock_agentcore.runtime import BedrockAgentCoreApp

from invoke_agent_utils import invoke_agent_with_boto3

logger = logging.getLogger(__name__)

app = BedrockAgentCoreApp()

def get_agent_arn(agent_name: str) -> str:
    """
    Retrieve agent ARN from Parameter Store
    """
    try:
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(
            Name=f'/agents/{agent_name}_arn'
        )
        if 'Parameter' not in response:
            response = ssm.get_parameter(
                Name=f'/agents/{agent_name}/arn'
            )
        return response['Parameter']['Value']
    except Exception as err:
        print(err)
        raise err

@tool
def call_tech_agent(user_query):
    """ call the tech agent """ 
    # print("Calling tech agent")
    try:
        tech_agent_arn = get_agent_arn ("mahen_tech_agent")
        result = invoke_agent_with_boto3(tech_agent_arn, user_query=user_query)
    except Exception as e:
        result = str(e)
        logger.exception("Exception calling tech agent: ")
    return result

@tool
def call_HR_agent(user_query):
    """ Get the HR agent """ 
    print("Calling HR agent")
    try:
        hr_agent_arn = get_agent_arn("mahen_hr_agent")
        print(hr_agent_arn)
        result = invoke_agent_with_boto3(hr_agent_arn, user_query=user_query)
    except Exception as e:
        result = str(e)
        logger.error(f"Exception calling hr agent: {e}", exc_info=True)
    return result


model_id = "us.amazon.nova-pro-v1:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    system_prompt="You're a helpful assistant, your role is to understand user questions and delegate to the appropriate specialized agent, you have tools to call the tech and HR agents",
    tools=[call_tech_agent, call_HR_agent]
)

def parse_event(event):
    """
    Parse a streaming event from the agent and return formatted output
    """
    # Skip events that don't need to be displayed
    if any(key in event for key in ['init_event_loop', 'start', 'start_event_loop']):
        return ""

    # Text chunks from supervisor
    if 'data' in event and isinstance(event['data'], str):
        return event['data'] 


    # Handle text messages from the assistant
    if 'event' in event:
        event_data = event['event']

        # Beginning of a tool use
        if 'contentBlockStart' in event_data and 'start' in event_data['contentBlockStart']:
            if 'toolUse' in event_data['contentBlockStart']['start']:
                tool_info = event_data['contentBlockStart']['start']['toolUse']
                return f"\n\n[Executing: {tool_info['name']}]\n\n"        

    return ""

@app.entrypoint
async def strands_agent_bedrock_streaming(payload):
    """
    Invoke the agent with streaming capabilities
    This function demonstrates how to implement streaming responses
    with AgentCore Runtime using async generators
    """
    user_input = payload.get("prompt")
    #print("User input:", user_input)

    try:
        # Stream each chunk as it becomes available
        async for event in agent.stream_async(user_input):
            text = parse_event(event)
            if text:  # Only return non-empty responses
                yield text

            #if "data" in event:
            #    yield event["data"]

    except Exception as e:
        # Handle errors gracefully in streaming context
        error_response = {"error": str(e), "type": "stream_error"}
        print(f"Streaming error: {error_response}")
        yield error_response


if __name__ == "__main__":
    app.run()
