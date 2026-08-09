from langchain_core.messages import SystemMessage, AIMessage
from datetime import datetime

from llm import llm
from prompts.planner_prompt import PLANNER_PROMPT
from utils.context import prepare_messages
from tools.employee.balance_tool import get_balance
from tools.employee.leave_tool import (
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
    modify_leave_request,
    cancel_leave_request

)
from tools.employee.policy_tool import search_policy
from tools.employee.policy_tool import search_policy

from tools.manager.team_leave_tools import (
    get_pending_team_leave_requests,
)

from tools.manager.approval_tools import (
    approve_leave_request,
    reject_leave_request,
)

from tools.manager.conflict_tool import (
    detect_team_conflicts,
)

# Bind tools to Claude
llm_with_tools = llm.bind_tools(
    [
        get_balance,
        list_leave_requests,
        validate_leave_request,
        submit_leave_request,
        modify_leave_request,
        search_policy,
        cancel_leave_request,
        get_pending_team_leave_requests,
        approve_leave_request,
        reject_leave_request,
        detect_team_conflicts
    ]
)


def planner_node(state):

    employee = state["employee"]
    if employee is None:
        return {
            "messages": [
                AIMessage(
                    content=(
                        "❌ I couldn't verify your employee account.\n\n"
                        "Please sign in again and try again."
                    )
                )
            ]
        }
    
    today = datetime.today()
    current_date = today.strftime("%Y-%m-%d")
    current_weekday = today.strftime("%A")

    system_prompt = SystemMessage(
        content=f"""
Employee Information

employee_id: {employee['employee_id']}
Name: {employee['name']}
Country: {employee['country']}
Department: {employee['department']}
Current Date: {current_date}
Current Weekday: {current_weekday}

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