from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from state.state import PTOState
from nodes.context_manager import context_manager_node
from nodes.load_context import load_context_node
from nodes.planner import planner_node
from nodes.extract_leave_details import extract_leave_details

from tools.balance_tool import get_balance
from tools.employee_tool import get_employee
from tools.leave_tool import (
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
)
from tools.policy_tool import search_policy

tools = [
    get_employee,
    get_balance,
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    search_policy,
]

builder = StateGraph(PTOState)

builder.add_node("load_context", load_context_node)
builder.add_node("planner", planner_node)
builder.add_node("tools", ToolNode(tools))
builder.add_node("context_manager", context_manager_node)
builder.add_node(
    "extract_leave_details",
    extract_leave_details
)

builder.add_edge(START, "load_context")
builder.add_edge("load_context", "context_manager")
builder.add_edge(
    "context_manager",
    "extract_leave_details"
)

builder.add_edge(
    "extract_leave_details",
    "planner"
)

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