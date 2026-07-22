from langchain_core.messages import HumanMessage, SystemMessage

from llm import llm
from schemas.leave_extraction import LeaveExtraction


EXTRACTION_PROMPT = """
You extract leave request details from the latest user message.

You are also given the Current Leave Request, which contains
details already collected in previous turns.

Return ONLY the extracted fields.

Rules:

1. Only extract information explicitly provided by the user.
2. Never guess missing information.
3. If the user only provides one missing field, update ONLY that field.
4. Do NOT overwrite existing values unless the user is clearly correcting them.
5. If the Current Leave Request already contains a value, leave it as null unless the user explicitly changes it.
"""

structured_llm = llm.with_structured_output(LeaveExtraction)


def extract_leave_details(state):

    pending = state.get("pending_leave", {}).copy()

    last_user = None

    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_user = msg
            break

    if last_user is None:
        return {}

    extracted = structured_llm.invoke(
        [
            SystemMessage(
                content=f"""
{EXTRACTION_PROMPT}

Current Leave Request

Leave Type: {pending.get("leave_type")}
Start Date: {pending.get("start_date")}
End Date: {pending.get("end_date")}
Reason: {pending.get("reason")}
"""
            ),
            HumanMessage(content=last_user.content),
        ]
    )

    extracted = extracted.model_dump()

    for key, value in extracted.items():
        if value is not None:
            pending[key] = value

    print("\nUpdated Pending Leave")
    print(pending)

    return {
        "pending_leave": pending
    }