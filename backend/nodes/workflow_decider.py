from langchain_core.messages import SystemMessage

from llm import llm
from prompts.workflow_decider_prompt import WORKFLOW_DECIDER_PROMPT


def workflow_decider_node(state):

    history = state["messages"]

    response = llm.invoke(
        [
            SystemMessage(content=WORKFLOW_DECIDER_PROMPT),
            *history,
        ]
    )

    content = response.content

    # The LLM may return either a string or a list of content blocks

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

    print("\n========== Workflow Decider ==========")
    print("Conversation:")

    for m in history:
        print(f"{m.type}: {m.content}")

    print(f"\nLLM Response : {answer}")
    print("=======================================\n")

    can_proceed = "PROCEED" in answer

    return {
        "workflow_decision": answer,
        "can_proceed": can_proceed,
    }