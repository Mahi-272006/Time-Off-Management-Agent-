from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from state.state import PTOState

from nodes.load_context import load_context_node
from nodes.context_manager import context_manager_node
from nodes.intent_classifier import intent_classifier_node
from nodes.clarify import clarify_node
from nodes.planner import planner_node

from tools.employee_tool import get_employee
from tools.balance_tool import get_balance
from tools.leave_tool import (
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request
)
from tools.policy_tool import search_policy


tools = [
    get_employee,
    get_balance,
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request,  
    search_policy,
]


builder = StateGraph(PTOState)

# -------------------------
# Nodes
# -------------------------

builder.add_node("load_context", load_context_node)
builder.add_node("context_manager", context_manager_node)
builder.add_node("intent_classifier", intent_classifier_node)
builder.add_node("clarify", clarify_node)
builder.add_node("planner", planner_node)
builder.add_node("tools", ToolNode(tools))


# -------------------------
# Routing Functions
# -------------------------

def route_after_intent(state):
    """
    Decide whether we have enough information
    to continue or need clarification.
    """

    if state.get("intent") == "AMBIGUOUS":
        return "clarify"

    return "planner"


# -------------------------
# Graph
# -------------------------

builder.add_edge(START, "load_context")

builder.add_edge("load_context", "context_manager")

builder.add_edge("context_manager", "intent_classifier")


builder.add_conditional_edges(
    "intent_classifier",
    route_after_intent,
    {
        "clarify": "clarify",
        "planner": "planner",
    },
)

builder.add_edge("clarify", END)


builder.add_conditional_edges(
    "planner",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END,
    },
)

builder.add_edge("tools", "planner")


graph = builder.compile()