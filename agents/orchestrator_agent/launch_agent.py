import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.agent_management.configure_runtime import configure_runtime, check_status

orchestrator_agent_arn1 = "arn:aws:iam::471727841202:role/agentcore-orchestrator_agent-role"
response, orchestrator_agent_runtime = configure_runtime("mahen_orchestrator_agent", orchestrator_agent_arn1, "./orchestrator_agent.py")
orchestrator_launch_result = orchestrator_agent_runtime.launch()
orchestrator_agent_id = orchestrator_launch_result.agent_id
orchestrator_agent_arn = orchestrator_launch_result.agent_arn
print(orchestrator_agent_arn)