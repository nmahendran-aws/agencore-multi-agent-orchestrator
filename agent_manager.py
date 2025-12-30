#!/usr/bin/env python3
"""
Multi-Agent Management System
Main entry point for managing and validating agents
"""

import argparse
import sys
from utils.agent_validator import AgentValidator
from utils.parameter_store.store_arn_parameter import store_agent_arn_in_parameter_store

def main():
    parser = argparse.ArgumentParser(description='Multi-Agent Management System')
    parser.add_argument('action', choices=['validate', 'launch', 'status', 'invoke', 'store-arn'], 
                       help='Action to perform')
    parser.add_argument('--agent', default='tech_agent', help='Agent name (default: tech_agent)')
    parser.add_argument('--prompt', default='Hello, can you help me?', help='Prompt for invoke action')
    parser.add_argument('--arn', help='Agent ARN for store-arn action')
    parser.add_argument('--parameter', help='Parameter store name for ARN')
    
    args = parser.parse_args()
    
    # Agent configurations
    agents_config = {
        'tech_agent': {
            'name': 'mahen_tech_agent',
            'role_arn': 'arn:aws:iam::471727841202:role/agentcore-tech_agent-role',
            'file_path': './agents/tech_agent/tech_agent.py'
        }
    }
    
    if args.agent not in agents_config:
        print(f"❌ Unknown agent: {args.agent}")
        print(f"Available agents: {list(agents_config.keys())}")
        sys.exit(1)
    
    config = agents_config[args.agent]
    validator = AgentValidator(
        agent_name=config['name'],
        agent_role_arn=config['role_arn'],
        agent_file_path=config['file_path']
    )
    
    if args.action == 'validate':
        success = validator.validate_full_workflow(args.prompt)
        sys.exit(0 if success else 1)
        
    elif args.action == 'launch':
        validator.configure_agent()
        agent_arn = validator.launch_agent()
        if agent_arn:
            print(f"Agent ARN: {agent_arn}")
        
    elif args.action == 'status':
        validator.configure_agent()
        validator.check_status()
        
    elif args.action == 'invoke':
        validator.configure_agent()
        validator.invoke_agent(args.prompt)
        
    elif args.action == 'store-arn':
        if not args.arn or not args.parameter:
            print("❌ --arn and --parameter are required for store-arn action")
            sys.exit(1)
        store_agent_arn_in_parameter_store(args.parameter, args.arn)

if __name__ == "__main__":
    main()