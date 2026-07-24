from utils.message_trimmer import trim_last_turns

MAX_TURNS = 5


def context_manager_node(state):
    """
    Keep only the last few complete conversation turns.
    """

    messages = state["messages"]

    trimmed = trim_last_turns(
        messages,
        max_turns=MAX_TURNS,
    )

    print("\n========== CONTEXT ==========")
    print("Messages before:", len(messages))
    print("Messages after :", len(trimmed))
    print("=============================\n")

    return {
        "messages": trimmed
    }