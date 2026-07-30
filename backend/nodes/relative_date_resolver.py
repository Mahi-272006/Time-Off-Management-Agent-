from datetime import datetime
import re

import dateparser
from langchain_core.messages import HumanMessage


def relative_date_resolver_node(state):
    """
    Converts relative dates like:
    - tomorrow
    - today
    - next Monday
    - this Friday
    - in 3 days

    into absolute dates before the planner sees them.
    """

    messages = state["messages"]

    if not messages:
        return {}

    last = messages[-1]

    if not isinstance(last, HumanMessage):
        return {}

    text = last.content

    base = datetime.now()

    settings = {
        "RELATIVE_BASE": base,
        "PREFER_DATES_FROM": "future",
    }

    replacements = {}

    patterns = [
        r"day after tomorrow",
        r"tomorrow",
        r"today",
        r"yesterday",
        r"next\s+\w+",
        r"this\s+\w+",
        r"in\s+\d+\s+days?",
    ]

    for pattern in patterns:

        for match in re.finditer(pattern, text, re.IGNORECASE):

            phrase = match.group()

            parsed = dateparser.parse(
                phrase,
                settings=settings,
            )

            if parsed:
                replacements[phrase] = parsed.strftime("%d %B %Y")

    new_text = text

    for old, new in replacements.items():
        new_text = re.sub(
            re.escape(old),
            new,
            new_text,
            flags=re.IGNORECASE,
        )

    if new_text != text:

        print("\n========== DATE RESOLUTION ==========")
        print("Original :", text)
        print("Resolved :", new_text)
        print("=====================================\n")

        messages[-1] = HumanMessage(content=new_text)

    return {
        "messages": messages
    }