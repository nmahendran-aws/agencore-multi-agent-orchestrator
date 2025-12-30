from utils.agent_management.configure_runtime import configure_runtime

tech_agent_arn1 = "arn:aws:iam::471727841202:role/agentcore-tech_agent-role"
response, tech_agent_runtime = configure_runtime("mahen_tech_agent", tech_agent_arn1, "./agents/tech_agent/tech_agent.py")

# Invoke the agent with proper payload format
payload = {
    "prompt": "Hello, can you help me with a technical question?"
}

invoke_response = tech_agent_runtime.invoke(payload)
print("Agent Response:", invoke_response['response'][0])