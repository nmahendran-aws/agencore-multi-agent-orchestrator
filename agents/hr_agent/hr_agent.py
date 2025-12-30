from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import argparse
import json
import operator
import math

app = BedrockAgentCoreApp()

@tool
def get_vacation_info():
    """Get remaining vacation days balance for the current year"""  # Dummy implementation
    return "you have 12 days off remaining this year"

# Define the agent using manual LangGraph construction
def create_agent():
    """Create and configure the LangGraph agent"""
    from langchain_aws import ChatBedrock

    # Initialize your LLM (adjust model and parameters as needed)
    llm = ChatBedrock(
        model_id="us.amazon.nova-pro-v1:0",  # or your preferred model
        model_kwargs={"temperature": 0.1}
    )

    # Bind tools to the LLM
    tools = [get_vacation_info]
    llm_with_tools = llm.bind_tools(tools)

    # System message
    system_message = f"""You're a helpful hr support assistant, you can answers user questions on vacations and benefits. 
    Here are the primary company benefits
    - Comprehensive health insurance with 100% premium coverage for employees and 75% for dependents
    - Flexible PTO policy with 20 days paid vacation annually, plus 5 sick days
    - 401(k) plan with 6% company matching and immediate vesting
    - Monthly wellness stipend of $100 for gym memberships or fitness activities

    For additional HR information instruct the user to call to 1-800-ASKHR"""

    # Define the chatbot node
    def chatbot(state: MessagesState):
        # Add system message if not already present
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_message)] + messages

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # Create the graph
    graph_builder = StateGraph(MessagesState)

    # Add nodes
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", ToolNode(tools))

    # Add edges
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")

    # Set entry point
    graph_builder.set_entry_point("chatbot")

    # Compile the graph
    return graph_builder.compile()

# Initialize the agent
agent = create_agent()

@app.entrypoint
def langgraph_bedrock(payload):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")

    # Create the input in the format expected by LangGraph
    response = agent.invoke({"messages": [HumanMessage(content=user_input)]})

    # Extract the final message content
    return response["messages"][-1].content

if __name__ == "__main__":
    app.run()
