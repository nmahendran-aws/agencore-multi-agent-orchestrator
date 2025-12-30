import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.agent_management.configure_runtime import configure_runtime, check_status

# Get the existing runtime without reconfiguring
hr_agent_arn1 = "arn:aws:bedrock-agentcore:us-east-1:471727841202:runtime/mahen_hr_agent-TnJnXMCleG"
response, hr_agent_runtime = configure_runtime("mahen_hr_agent", hr_agent_arn1, "./hr_agent.py")

# Just check status of existing deployment
status_response = hr_agent_runtime.status()
#print("Tech Agent runtime:", tech_agent_runtime.endpoint['endpointName'])
print("Agent Status:", status_response.endpoint['status'])