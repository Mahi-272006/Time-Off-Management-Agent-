from langchain_core.messages import SystemMessage

from llm import llm
from prompts.intent_classifier_prompt import INTENT_CLASSIFIER_PROMPT


def intent_classifier_node(state):

    history = state["messages"]

    response = llm.invoke(
        [
            SystemMessage(content=INTENT_CLASSIFIER_PROMPT),
            *history,
        ]
    )

    answer = response.content.strip().upper()

    can_proceed = answer == "PROCEED"

    return {
        "can_proceed": can_proceed
    }