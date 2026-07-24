
from langchain_core.messages import SystemMessage

from llm import llm
from utils.context import prepare_messages
from prompts.intent_classifier_prompt import INTENT_CLASSIFIER_PROMPT

def intent_classifier_node(state):

    history = state["messages"]

    response = llm.invoke(
        [
            SystemMessage(content=INTENT_CLASSIFIER_PROMPT),
            *history,
        ]
    )

    intent = response.content.strip().upper()

    print("\n========== INTENT CLASSIFIER ==========")
    print("Conversation:")
    for m in history:
        print(f"{m.type}: {m.content}")
    print(f"\nPredicted Intent: {intent}")
    print("=======================================\n")

    return {"intent": intent}