def route_after_intent(state):

    if state["intent"] == "AMBIGUOUS":
        return "clarify"

    return "planner"