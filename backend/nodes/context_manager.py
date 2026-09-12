from langchain_core.messages import HumanMessage

#last 8 messages only
MAX_TURNS = 8


def trim_last_turns(messages, max_turns=MAX_TURNS):
    """
    Keep only the last N complete conversation turns.

    A conversation turn starts with a HumanMessage
    and includes all AI/Tool messages until the next HumanMessage.

    This prevents ToolMessages from being separated
    from the AI message that generated them.
    """

    if not messages:
        return []

    turns = []   #contains turn1,turn2,turn3....
    current_turn = []  #contains message belongs to the current turn 

    for msg in messages:

        # New user message → previous turn finished
        if isinstance(msg, HumanMessage):

            #When the next HumanMessage arrives, this entire group gets added to turns
            if current_turn:
                turns.append(current_turn)

            current_turn = [msg]

        #handles everything that isn't a HumanMessage
        else:
            current_turn.append(msg)

    # Add final turn
    if current_turn:
        turns.append(current_turn)

    # Keep only the last N turns
    turns = turns[-max_turns:]

    #Convert turns back to messages
    trimmed = []

    for turn in turns:
        trimmed.extend(turn)

    return trimmed


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