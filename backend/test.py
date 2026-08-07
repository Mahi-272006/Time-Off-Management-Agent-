from graph import graph
from langchain_core.messages import HumanMessage

# ==========================================================
# Initial State
# ==========================================================

state = {
    "employee_id": "EMP002",
    "messages": [],
    "summary": "",
}

# ==========================================================
# Thread ID (required if using MemorySaver/checkpointer)
# ==========================================================

thread_id = state["employee_id"]

# ==========================================================
# Banner
# ==========================================================

print("=" * 70)
print("Acme Time-Off Agent")
print("=" * 70)
print("Type 'exit' to quit.")

# ==========================================================
# Test Cases
# ==========================================================

# Uncomment any one test suite

# test_cases = [
#     "Show my leave balance"
# ]

# test_cases = [
#     "Take annual leave tomorrow"
# ]

# test_cases = [
#     "Take leave tomorrow",
#     "Annual",
#     "One day"
# ]

# test_cases = [
#     "Show my balance and take sick leave tomorrow"
# ]

# test_cases = [
#     "Show my leave history and explain sick leave policy"
# ]

# Interactive mode
test_cases = None

# ==========================================================
# Interactive Mode
# ==========================================================

if test_cases is None:

    while True:

        user_input = input("\nUSER: ")

        if user_input.lower() in ["exit", "quit"]:
            print("\nConversation Finished.")
            break

        state["messages"].append(
            HumanMessage(content=user_input)
        )

        state = graph.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        print("\nBOT:\n")

        last_message = state["messages"][-1]

        if hasattr(last_message, "content"):
            print(last_message.content)
        else:
            print(last_message)

# ==========================================================
# Automatic Test Cases
# ==========================================================

else:

    for user_input in test_cases:

        print("\nUSER:", user_input)

        state["messages"].append(
            HumanMessage(content=user_input)
        )

        state = graph.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        print("\nBOT:\n")

        last_message = state["messages"][-1]

        if hasattr(last_message, "content"):
            print(last_message.content)
        else:
            print(last_message)

    print("\nConversation Finished.")