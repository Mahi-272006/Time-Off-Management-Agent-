from langchain_core.messages import HumanMessage


def trim_last_turns(messages, max_turns=5):
    """
    Keep only the last N complete conversation turns.

    A conversation turn starts with a HumanMessage and
    includes every AI/Tool message until the next HumanMessage.

    This guarantees that ToolMessages are never separated
    from the AI message that generated them.
    """

    if not messages:
        return []

    turns = []
    current_turn = []

    for msg in messages:

        # New user message → previous turn finished
        if isinstance(msg, HumanMessage):

            if current_turn:
                turns.append(current_turn)

            current_turn = [msg]

        else:
            current_turn.append(msg)

    # Add final turn
    if current_turn:
        turns.append(current_turn)

    # Keep only last N turns
    turns = turns[-max_turns:]

    trimmed = []

    for turn in turns:
        trimmed.extend(turn)

    return trimmed