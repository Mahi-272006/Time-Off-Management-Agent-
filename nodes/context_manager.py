from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

MAX_MESSAGES = 10

def context_manager_node(state):
    """
    Keep only the most recent messages to avoid
    sending the entire conversation to the LLM.
    """

    messages = state["messages"]

    # Nothing to trim
    if len(messages) <= MAX_MESSAGES:
        return {}

    trimmed_messages = messages[-MAX_MESSAGES:]

    return {
        "messages": trimmed_messages
    }