import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.agent_management.configure_runtime import configure_runtime

hr_agent_arn1 = "arn:aws:iam::471727841202:role/agentcore-hr_agent-role"
response, hr_agent_runtime = configure_runtime("mahen_hr_agent", hr_agent_arn1, "./hr_agent.py")

status_response = hr_agent_runtime.status()
print("Agent Status:", status_response.endpoint['status'])