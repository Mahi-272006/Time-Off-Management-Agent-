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
'''test_cases = [
    # 1. Greeting
    "Hi",

    # 2. Balance
    "Show my leave balance",

    # 3. Leave history
    "Show my leave history",

    # 4. Policy
    "What is the annual leave policy?",

    # 5. New leave - complete
    "Take annual leave on 20 August 2026",

    # 6. Missing leave type
    "Take leave on 21 August 2026",

    # 7. Missing date
    "Take sick leave",

    # 8. Relative date
    "Take annual leave tomorrow",

    # 9. Synonym
    "Take PTO on 25 August 2026",

    # 10. Multi-day leave
    "Take annual leave from 1 September 2026 to 3 September 2026",

    # 11. Multi-intent
    "Show my balance and take sick leave on 5 September 2026",

    # 12. Policy + history
    "Show my leave history and explain the sick leave policy",

    # 13. Invalid date
    "Take annual leave on 31 February 2026",

    # 14. Modify existing request
    "Actually move my leave request to 28 August 2026",

    # 15. Cancel existing request
    "Cancel my latest leave request"
]'''
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