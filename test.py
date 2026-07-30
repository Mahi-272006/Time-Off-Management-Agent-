from graph import graph

state = {
    "employee_id": "EMP002",
    "messages": [],
    "summary": ""
}

print("=" * 70)
print("Acme Time-Off Agent")
print("=" * 70)
print("Type 'exit' to quit.")

# ==========================================================
# Choose ONE test suite by uncommenting it
# ==========================================================

# ---------- 1. Greeting ----------
# test_cases = [
#     "Hi"
# ]

# ---------- 2. Balance ----------
# test_cases = [
#     "Show my leave balance"
# ]

# ---------- 3. Leave History ----------
# test_cases = [
#     "Show my leave history"
# ]

# ---------- 4. Annual Leave Policy ----------
# test_cases = [
#     "What is the annual leave policy?"
# ]

# ---------- 5. Sick Leave Policy ----------
# test_cases = [
#     "Explain the sick leave policy"
# ]

# ---------- 6. Parental Leave Policy ----------
# test_cases = [
#     "Tell me about parental leave"
# ]

# ---------- 7. All Policies ----------
# test_cases = [
#     "Explain all leave policies"
# ]

# ---------- 8. Relative Date ----------
# test_cases = [
#     "Take annual leave tomorrow"
# ]

# ---------- 9. Missing Leave Type ----------
# test_cases = [
#     "Take leave tomorrow"
# ]

# ---------- 10. Missing Date ----------
# test_cases = [
#     "Take sick leave"
# ]

# ---------- 11. Multi-Day Leave ----------
# test_cases = [
#     "Take annual leave from 10 August to 14 August"
# ]

# ---------- 12. Multi-Intent ----------
# test_cases = [
#     "Show my balance and take sick leave tomorrow"
# ]

# ---------- 13. Multi-Intent ----------
# test_cases = [
#     "Show my leave history and explain sick leave policy"
# ]

# ---------- 14. Modify Leave ----------
# test_cases = [
#     "Take annual leave tomorrow",
#     "Actually make it Friday"
# ]

# ---------- 15. Modify Leave Type ----------
# test_cases = [
#     "Take annual leave tomorrow",
#     "Actually make it sick leave"
# ]

# ---------- 16. Extend Leave ----------
# test_cases = [
#     "Take annual leave tomorrow",
#     "Extend it by two days"
# ]

# ---------- 17. Cancel by ID ----------
# test_cases = [
#     "Cancel request 2"
# ]

# ---------- 18. Cancel by Conversation ----------
# test_cases = [
#     "Take annual leave tomorrow",
#     "Cancel it"
# ]

# ---------- 19. Pronoun Resolution ----------
# test_cases = [
#     "Take sick leave tomorrow",
#     "Move it to Friday"
# ]

# ---------- 20. Synonyms ----------
# test_cases = [
#     "Take PTO tomorrow"
# ]

# ---------- 21. Medical Leave Synonym ----------
# test_cases = [
#     "I need medical leave tomorrow"
# ]

# ---------- 22. Full End-to-End Conversation ----------
'''test_cases = [
   "Hi",
   "What are all my leave policies?",
   "Show my balance",
    "Take annual leave tomorrow",
    "Actually make it Friday",
    "Show my leave history",
    "Cancel it",
    "Show my leave history"
]'''

# ---------- Interactive Mode ----------
test_cases = None

# ==========================================================

if test_cases is None:

    while True:

        user_input = input("\nUSER: ")

        if user_input.lower() in ["exit", "quit"]:
            print("\nConversation Finished.")
            break

        state["messages"].append(
            {
                "role": "user",
                "content": user_input
            }
        )

        state = graph.invoke(state)

        print("\nBOT:")

        last_message = state["messages"][-1]

        if hasattr(last_message, "content"):
            print(last_message.content)
        else:
            print(last_message)

else:

    for user_input in test_cases:

        print("\nUSER:", user_input)

        state["messages"].append(
            {
                "role": "user",
                "content": user_input
            }
        )

        state = graph.invoke(state)

        print("\nBOT:")

        last_message = state["messages"][-1]

        if hasattr(last_message, "content"):
            print(last_message.content)
        else:
            print(last_message)

    print("\nConversation Finished.")