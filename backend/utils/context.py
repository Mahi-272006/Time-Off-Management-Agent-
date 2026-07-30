from langchain_core.messages import SystemMessage


def prepare_messages(system_prompt, state):
    """
    Build the messages sent to the LLM.

    Includes:
    - System prompt
    - Conversation summary (optional)
    - Trimmed conversation history
    """

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

    prompt.extend(state["messages"])

    return prompt