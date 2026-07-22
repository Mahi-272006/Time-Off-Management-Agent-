from typing import TypedDict, Annotated, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class PendingLeave(TypedDict):
    leave_type: str | None
    start_date: str | None
    end_date: str | None
    reason: str | None


class PTOState(TypedDict):
    # Conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Current employee
    employee_id: str

    # Employee details loaded from tool
    employee: dict[str, Any]

    # Tool outputs
    tool_results: dict[str, Any]

    # Retrieved RAG documents
    retrieved_docs: list

    # Final response
    final_response: str

    # Clarification handling
    needs_clarification: bool
    clarification_question: str

    # Conversation memory
    summary: str

    # Multi-turn leave request
    pending_leave: PendingLeave