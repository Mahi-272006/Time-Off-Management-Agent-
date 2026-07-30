from langchain_core.messages import SystemMessage

from llm import llm
from prompts.planner_prompt import PLANNER_PROMPT
from utils.context import prepare_messages

from tools.employee_tool import get_employee
from tools.balance_tool import get_balance
from tools.leave_tool import (
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request,
    cancel_leave_request
)
from tools.policy_tool import search_policy


# Bind tools to Claude
llm_with_tools = llm.bind_tools(
    [
        get_employee,
        get_balance,
        list_leave_requests,
        validate_leave_request,
        submit_leave_request,
        modify_leave_request,
        search_policy,
        cancel_leave_request,
    ]
)


def planner_node(state):

    employee = state["employee"]

    system_prompt = SystemMessage(
        content=f"""
Employee Information

employee_id: {employee['employee_id']}
Name: {employee['name']}
Country: {employee['country']}
Department: {employee['department']}

{PLANNER_PROMPT}
"""
    )

    prompt = prepare_messages(system_prompt, state)

    print("\n" + "=" * 100)
    print("PROMPT SENT TO CLAUDE")
    print("=" * 100)

    for i, msg in enumerate(prompt):
        print(f"\n[{i}] {type(msg).__name__}")

        if hasattr(msg, "tool_call_id"):
            print("Tool Call ID:", msg.tool_call_id)

        print(msg.content)

    print("=" * 100)
    response = llm_with_tools.invoke(prompt)

    response = llm_with_tools.invoke(prompt)

    print("\n========================")
    print("CONTENT:")
    print(response.content)
    print("TOOL CALLS:")
    print(response.tool_calls)
    print("========================")

    return {
        "messages": [response]
    }