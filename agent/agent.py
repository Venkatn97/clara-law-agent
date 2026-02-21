import os
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from agent.prompts import CLARA_SYSTEM_PROMPT
from agent.tools import ALL_TOOLS
from agent.memory import AgentState, create_initial_state

load_dotenv()


def build_clara_agent():

    llm = ChatBedrock(
        model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        model_kwargs={"temperature": 0.3, "max_tokens": 1024},

        guardrails={
        "guardrailIdentifier": os.getenv("4meaya3z1ebi"),
        "guardrailVersion": os.getenv("BEDROCK_GUARDRAIL_VERSION", "DRAFT"),
        "trace": "enabled"
    }
    )

    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    def agent_node(state: AgentState) -> dict:
        messages = [SystemMessage(content=CLARA_SYSTEM_PROMPT)] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(ALL_TOOLS)

    def should_continue(state: AgentState) -> str:
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            tool_names = [tc["name"] for tc in last_message.tool_calls]
            print(f"\n🔧 Clara is calling: {', '.join(tool_names)}")
            return "tools"
        return END

    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )

    workflow.add_edge("tools", "agent")

    return workflow.compile()


clara = build_clara_agent()


def chat(user_message: str, state: AgentState):
    state["messages"].append(HumanMessage(content=user_message))
    result = clara.invoke(state)
    last_message = result["messages"][-1]
    return last_message.content, result


def run_single_query(query: str) -> str:
    state = create_initial_state(session_id="test-single")
    response, _ = chat(query, state)
    return response