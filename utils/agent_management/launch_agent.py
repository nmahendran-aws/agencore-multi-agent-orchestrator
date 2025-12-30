from utils.agent_management.configure_runtime import configure_runtime, check_status

tech_agent_arn1 = "arn:aws:iam::471727841202:role/agentcore-tech_agent-role"
response, tech_agent_runtime = configure_runtime("mahen_tech_agent", tech_agent_arn1, "./agents/tech_agent/tech_agent.py")
tech_launch_result = tech_agent_runtime.launch()
tech_agent_id = tech_launch_result.agent_id
tech_agent_arn = tech_launch_result.agent_arn

print(tech_agent_arn)