from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import time
import os


def configure_runtime(agent_name, agentcore_iam_role, python_file_name):
    boto_session = Session(region_name=os.getenv("AWS_DEFAULT_REGION"))
    region = boto_session.region_name

    agentcore_runtime = Runtime()

    response = agentcore_runtime.configure(
        entrypoint=python_file_name,
        execution_role=agentcore_iam_role,
        auto_create_ecr=True,
        requirements_file="requirements.txt",
        region=region,
        agent_name=agent_name
    )
    return response, agentcore_runtime

def check_status(agent_runtime):
    status_response = agent_runtime.status()
    status = status_response.endpoint['status']
    end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
    while status not in end_status:
        time.sleep(10)
        status_response = agent_runtime.status()
        status = status_response.endpoint['status']
        print(status)
    return status