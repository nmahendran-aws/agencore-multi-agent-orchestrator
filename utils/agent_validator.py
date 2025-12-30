import boto3
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.agent_management.configure_runtime import configure_runtime
from utils.parameter_store.invoke_from_parameter_store import get_agent_arn_from_parameter_store

class AgentValidator:
    def __init__(self, agent_name, agent_role_arn, agent_file_path, region='us-east-1'):
        self.agent_name = agent_name
        self.agent_role_arn = agent_role_arn
        self.agent_file_path = agent_file_path
        self.region = region
        self.runtime = None
        
    def configure_agent(self):
        """Configure the agent runtime"""
        try:
            response, self.runtime = configure_runtime(
                self.agent_name, 
                self.agent_role_arn, 
                self.agent_file_path
            )
            print(f"✅ Agent {self.agent_name} configured successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to configure agent {self.agent_name}: {e}")
            return False
    
    def check_status(self):
        """Check agent status"""
        if not self.runtime:
            print("❌ Runtime not configured. Call configure_agent() first.")
            return None
            
        try:
            status_response = self.runtime.status()
            status = status_response.endpoint['status']
            print(f"📊 Agent Status: {status}")
            return status
        except Exception as e:
            print(f"❌ Failed to check status: {e}")
            return None
    
    def launch_agent(self):
        """Launch the agent"""
        if not self.runtime:
            print("❌ Runtime not configured. Call configure_agent() first.")
            return None
            
        try:
            launch_result = self.runtime.launch()
            agent_arn = launch_result.agent_arn
            print(f"🚀 Agent launched successfully: {agent_arn}")
            return agent_arn
        except Exception as e:
            print(f"❌ Failed to launch agent: {e}")
            return None
    
    def invoke_agent(self, prompt):
        """Invoke the agent with a prompt"""
        if not self.runtime:
            print("❌ Runtime not configured. Call configure_agent() first.")
            return None
            
        try:
            payload = {"prompt": prompt}
            response = self.runtime.invoke(payload)
            result = response['response'][0]
            print(f"💬 Agent Response: {result}")
            return result
        except Exception as e:
            print(f"❌ Failed to invoke agent: {e}")
            return None
    
    def invoke_direct(self, agent_arn, prompt):
        """Invoke agent directly using ARN"""
        try:
            client = boto3.client('bedrock-agentcore', region_name=self.region)
            payload = {"prompt": prompt}
            
            response = client.invoke_agent_runtime(
                agentRuntimeArn=agent_arn,
                payload=json.dumps(payload)
            )
            
            result = response['response'].read().decode('utf-8')
            print(f"💬 Direct Agent Response: {result}")
            return result
        except Exception as e:
            print(f"❌ Failed to invoke agent directly: {e}")
            return None
    
    def invoke_from_parameter_store(self, parameter_name, prompt):
        """Invoke agent using ARN from parameter store"""
        try:
            agent_arn = get_agent_arn_from_parameter_store(parameter_name, self.region)
            if not agent_arn:
                print(f"❌ Failed to retrieve ARN from parameter {parameter_name}")
                return None
                
            return self.invoke_direct(agent_arn, prompt)
        except Exception as e:
            print(f"❌ Failed to invoke from parameter store: {e}")
            return None
    
    def validate_full_workflow(self, test_prompt="Hello, can you help me?"):
        """Run full validation workflow"""
        print(f"🔍 Starting full validation for {self.agent_name}")
        
        # Step 1: Configure
        if not self.configure_agent():
            return False
            
        # Step 2: Check status
        status = self.check_status()
        if status != 'READY':
            print(f"⚠️  Agent status is {status}, attempting to launch...")
            agent_arn = self.launch_agent()
            if not agent_arn:
                return False
        
        # Step 3: Test invoke
        result = self.invoke_agent(test_prompt)
        if result:
            print("✅ Full validation completed successfully")
            return True
        else:
            print("❌ Validation failed")
            return False

# Example usage
if __name__ == "__main__":
    validator = AgentValidator(
        agent_name="mahen_tech_agent",
        agent_role_arn="arn:aws:iam::471727841202:role/agentcore-tech_agent-role",
        agent_file_path="./agents/tech_agent/tech_agent.py"
    )
    
    # Run full validation
    validator.validate_full_workflow("Hello, can you help me with a technical question?")