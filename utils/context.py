from langchain_core.messages import SystemMessage


MAX_MESSAGES = 10


def prepare_messages(system_prompt, state):
    """
    Returns the messages sent to the LLM.

    Includes:
    - system prompt
    - conversation summary (if any)
    - last few messages
    """

    messages = state["messages"]

    prompt = [system_prompt]

    if state.get("summary"):
        prompt.append(
            SystemMessage(
                content=f"""
Conversation Summary:

{state['summary']}
"""
            )
        )

    prompt.extend(messages[-MAX_MESSAGES:])

    return prompt