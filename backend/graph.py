from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage

from utils.authorization import is_tool_authorized
from state.state import PTOState

from nodes.load_emp_info import load_emp_info_node
from nodes.context_manager import context_manager_node
from nodes.workflow_decider import workflow_decider_node
from nodes.clarify import clarify_node
from nodes.planner import planner_node
from nodes.relative_date_resolver import relative_date_resolver_node


# Employee Tools
from tools.employee.balance_tool import get_balance

from tools.employee.leave_tool import (
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request,
    cancel_leave_request,
)

from tools.employee.policy_tool import search_policy


# Manager Tools
from tools.manager.conflict_tool import detect_team_conflicts

from tools.manager.team_leave_tools import (
    get_pending_team_leave_requests,
)

from tools.manager.approval_tools import (
    approve_leave_request,
    reject_leave_request,
)


# All Tools
tools = [
    get_balance,
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request,
    cancel_leave_request,
    search_policy,

    get_pending_team_leave_requests,
    approve_leave_request,
    reject_leave_request,
    detect_team_conflicts,
]


# Create ToolNode ONCE
tool_node = ToolNode(tools)


# Authorization Wrapper
def authorized_tools_node(state):

    role = state.get("role", "employee")

    last_message = state["messages"][-1]

    # Check every requested tool before executing anything
    for tool_call in last_message.tool_calls:

        tool_name = tool_call["name"]

        print(
            f"AUTHORIZATION CHECK | "
            f"role={role} | tool={tool_name}"
        )

        if not is_tool_authorized(tool_name, role):

            print(
                f"AUTHORIZATION DENIED | "
                f"role={role} | tool={tool_name}"
            )

            return {
                "messages": [
                    AIMessage(
                        content=(
                            "You are not authorized to perform "
                            "this action. Manager access is required."
                        )
                    )
                ],
                "can_proceed": False,
            }

    # All requested tools are authorized
    print(
        f"AUTHORIZATION PASSED | role={role}"
    )

    return tool_node.invoke(state)


# Graph
builder = StateGraph(PTOState)


# Nodes
builder.add_node(
    "load_emp_info",
    load_emp_info_node
)

builder.add_node(
    "context_manager",
    context_manager_node
)

builder.add_node(
    "relative_date_resolver",
    relative_date_resolver_node
)

builder.add_node(
    "workflow_decider",
    workflow_decider_node
)

builder.add_node(
    "clarify",
    clarify_node
)

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "tools",
    authorized_tools_node
)


# Memory
memory = MemorySaver()


# Routing Functions
def route_after_intent(state):

    if state.get("can_proceed"):
        return "planner"

    return "clarify"


# Graph Edges
builder.add_edge(
    START,
    "load_emp_info"
)

builder.add_edge(
    "load_emp_info",
    "context_manager"
)

builder.add_edge(
    "context_manager",
    "relative_date_resolver"
)

builder.add_edge(
    "relative_date_resolver",
    "workflow_decider"
)


# Workflow Decider
builder.add_conditional_edges(
    "workflow_decider",
    route_after_intent,
    {
        "clarify": "clarify",
        "planner": "planner",
    },
)


# Clarification ends the current turn
builder.add_edge(
    "clarify",
    END
)


# Planner decides whether a tool is required
builder.add_conditional_edges(
    "planner",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END,
    },
)


# Tool → Planner
builder.add_edge(
    "tools",
    "planner"
)


# Compile Graph
graph = builder.compile(
    checkpointer=memory
)