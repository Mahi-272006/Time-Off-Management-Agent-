def route_after_intent(state):

    if state["can_proceed"]:
        return "planner"

    return "clarify"