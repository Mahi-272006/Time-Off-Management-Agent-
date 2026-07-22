from langchain_core.messages import (
    SystemMessage,
    ToolMessage,
)

from llm import llm
from prompts.planner_prompt import PLANNER_PROMPT
from utils.context import prepare_messages

from tools.employee_tool import get_employee
from tools.balance_tool import get_balance
from tools.leave_tool import (
    list_leave_requests,
    validate_leave_request,
    submit_leave_request,
)
from tools.policy_tool import search_policy


# Bind all tools to the LLM
llm_with_tools = llm.bind_tools(
    [
        get_employee,
        get_balance,
        list_leave_requests,
        validate_leave_request,
        submit_leave_request,
        search_policy,
    ]
)


def planner_node(state):
    """
    Main reasoning node.

    Responsibilities:
    1. Understand the user's request.
    2. Decide whether a tool is required.
    3. Decide which tool to call.
    4. Ask follow-up questions if information is missing.
    5. Use the Current Leave Request as working memory.
    """

    employee = state["employee"]
    pending = state.get("pending_leave", {})

    system_prompt = SystemMessage(
        content=f"""
Employee ID: {state['employee_id']}
Employee Name: {employee['name']}
Employee Country: {employee['country']}
Department: {employee['department']}

Current Leave Request

Leave Type: {pending.get("leave_type")}
Start Date: {pending.get("start_date")}
End Date: {pending.get("end_date")}
Reason: {pending.get("reason")}

{PLANNER_PROMPT}
"""
    )

    # Build prompt using summary + recent messages
    prompt = prepare_messages(system_prompt, state)

    # Check the last message
    last_message = state["messages"][-1]

    clear_pending = (
        isinstance(last_message, ToolMessage)
        and last_message.name == "submit_leave_request"
    )

    # Claude decides what to do next
    response = llm_with_tools.invoke(prompt)

    result = {
        "messages": [response]
    }

    # Clear workflow memory after successful submission
    if clear_pending:
        print("\n✅ Clearing pending leave...\n")

        result["pending_leave"] = {
            "leave_type": None,
            "start_date": None,
            "end_date": None,
            "reason": None,
        }

    return result


     