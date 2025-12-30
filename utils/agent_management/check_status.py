from utils.agent_management.configure_runtime import configure_runtime, check_status

# Get the existing runtime without reconfiguring
tech_agent_arn1 = "arn:aws:iam::471727841202:role/agentcore-tech_agent-role"
response, tech_agent_runtime = configure_runtime("mahen_tech_agent", tech_agent_arn1, "./agents/tech_agent/tech_agent.py")

# Just check status of existing deployment
status_response = tech_agent_runtime.status()
#print("Tech Agent runtime:", tech_agent_runtime.endpoint['endpointName'])
print("Agent Status:", status_response.endpoint['status'])