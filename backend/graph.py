from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from state.state import PTOState

from nodes.load_context import load_context_node
from nodes.context_manager import context_manager_node
from nodes.intent_classifier import intent_classifier_node
from nodes.clarify import clarify_node
from nodes.planner import planner_node
from nodes.relative_date_resolver import relative_date_resolver_node
from tools.suggest_leave_tool import suggest_leave_dates
from tools.balance_tool import get_balance
from tools.leave_tool import (
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request,
    cancel_leave_request
)
from tools.policy_tool import search_policy


tools = [
    get_balance,
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request, 
    cancel_leave_request, 
    search_policy,
    suggest_leave_dates
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
builder.add_node(
    "relative_date_resolver",
    relative_date_resolver_node,
)


# -------------------------
# Routing Functions
# -------------------------

def route_after_intent(state):

    if state.get("can_proceed"):
        return "planner"

    return "clarify"


# -------------------------
# Graph
# -------------------------

builder.add_edge(START, "load_context")

builder.add_edge("load_context", "context_manager")

builder.add_edge(
    "context_manager",
    "relative_date_resolver",
)

builder.add_edge(
    "relative_date_resolver",
    "intent_classifier",
)


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