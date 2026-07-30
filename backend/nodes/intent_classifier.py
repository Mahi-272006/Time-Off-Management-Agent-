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

    content = response.content

    # Claude may return either a string or a list of content blocks
    if isinstance(content, str):
        answer = content.strip().upper()

    elif isinstance(content, list):
        texts = []

        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))

        answer = " ".join(texts).strip().upper()

    else:
        answer = str(content).strip().upper()

    print("\n========== INTENT CLASSIFIER ==========")
    print("Conversation:")

    for m in history:
        print(f"{m.type}: {m.content}")

    print(f"\nLLM Response : {answer}")
    print("=======================================\n")

    can_proceed = "PROCEED" in answer

    return {
        "intent": answer,
        "can_proceed": can_proceed,
    }