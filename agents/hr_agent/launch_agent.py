import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.agent_management.configure_runtime import configure_runtime, check_status

hr_agent_arn1 = "arn:aws:iam::471727841202:role/agentcore-hr_agent-role"
response, hr_agent_runtime = configure_runtime("mahen_hr_agent", hr_agent_arn1, "./hr_agent.py")
hr_launch_result = hr_agent_runtime.launch()
hr_agent_id = hr_launch_result.agent_id
hr_agent_arn = hr_launch_result.agent_arn

print(hr_agent_arn)