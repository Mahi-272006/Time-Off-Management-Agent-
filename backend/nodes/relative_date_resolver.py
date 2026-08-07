from datetime import datetime
import re

import dateparser
from langchain_core.messages import HumanMessage


def relative_date_resolver_node(state):
    """
    Resolves relative dates like:
        - today
        - tomorrow
        - day after tomorrow
        - next Monday
        - this Friday
        - in 3 days

    into absolute dates before the planner sees the message.
    """

    messages = state["messages"]

    if not messages:
        return {}

    last = messages[-1]

    if not isinstance(last, HumanMessage):
        return {}

    text = last.content

    settings = {
        "RELATIVE_BASE": datetime.now(),
        "PREFER_DATES_FROM": "future",
    }

    patterns = [
    r"day after tomorrow",
    r"tomorrow",
    r"today",
    r"yesterday",
    r"next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"this\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"in\s+\d+\s+days?",
    ]

    new_text = text

    for pattern in patterns:

        matches = re.finditer(pattern, text, re.IGNORECASE)

        for match in matches:

            phrase = match.group()

            parsed = dateparser.parse(
                phrase,
                settings=settings,
            )

            if parsed:

                absolute_date = parsed.strftime("%d %B %Y")

                new_text = re.sub(
                    re.escape(phrase),
                    absolute_date,
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