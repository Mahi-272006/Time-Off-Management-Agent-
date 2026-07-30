from langchain_core.messages import HumanMessage

RELATIVE_DATE_KEYWORDS = [
    "today",
    "tomorrow",
    "day after tomorrow",

    "next monday",
    "next tuesday",
    "next wednesday",
    "next thursday",
    "next friday",
    "next saturday",
    "next sunday",

    "this monday",
    "this tuesday",
    "this wednesday",
    "this thursday",
    "this friday",
    "this saturday",
    "this sunday",

    "in ",
]

LEAVE_KEYWORDS = [
    "leave",
    "vacation",
    "pto",
    "holiday",
    "book",
    "apply",
    "cancel",
    "modify",
    "request",
]


def date_router_node(state):

    text = state["messages"][-1].content.lower()

    has_relative_date = any(
        word in text
        for word in RELATIVE_DATE_KEYWORDS
    )

    return {
        "resolve_dates": has_relative_date
    }