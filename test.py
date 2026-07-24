from graph import graph

state = {
    "employee_id": "EMP002",
    "messages": [],
    "summary": ""
}

print("=" * 70)
print("Acme Time-Off Agent")
print("=" * 70)

# ============================================================
# TEST SUITES
# Uncomment ONE suite at a time.
# ============================================================

# ---------- TEST 1 : Normal Leave Request ----------
# test_cases = [
#     "Take annual leave from 10 Sep to 12 Sep."
# ]

# ---------- TEST 2 : Missing Information ----------
# test_cases = [
#     "I want a leave.",
#     "Annual leave",
#     "10 Sep to 12 Sep"
# ]

# ---------- TEST 3 : Vacation Normalization ----------
# test_cases = [
#     "Take vacation leave on 15 Aug."
# ]

# ---------- TEST 4 : Balance ----------
# test_cases = [
#     "How many sick leaves do I have?"
# ]

# ---------- TEST 5 : Policy ----------
# test_cases = [
#     "Can I carry forward annual leave?"
# ]

# ---------- TEST 6 : Leave History ----------
# test_cases = [
#     "Show my leave history."
# ]

# ---------- TEST 7 : Modify Latest Leave ----------
# test_cases = [
#     "Take sick leave on 27 Aug.",
#     "27 Aug itself.",
#     "Actually change it to 29 Aug."
# ]

# ---------- TEST 8 : Modify by Request ID ----------
# test_cases = [
#     "Change request id 11.",
#     "Start date should be 5 Nov."
# ]

# ---------- TEST 9 : Modify by Start Date ----------
# test_cases = [
#     "Modify the leave whose start date is 22 July 2025.",
#     "Change end date to 22 July.",
#     "Yes."
# ]

# ---------- TEST 10 : Overlap ----------
# test_cases = [
#     "Change request id 12.",
#     "Start date should be 6 Nov."
# ]

# ---------- TEST 11 : Cancel Latest ----------
# test_cases = [
#     "Take sick leave on 27 Aug.",
#     "27 Aug.",
#     "Actually cancel it."
# ]

# ---------- TEST 12 : Cancel by ID ----------
# test_cases = [
#     "Cancel request id 11."
# ]

# ---------- TEST 13 : Cancel Multiple ----------
# test_cases = [
#     "Cancel request id 13 and 14."
# ]

# ---------- TEST 14 : Ambiguous Cancel ----------
# test_cases = [
#     "Cancel my leave.",
#     "5"
# ]

# ---------- TEST 15 : Multi Intent ----------
# test_cases = [
#     "Take annual leave on 15 Aug and also tell me my balance."
# ]

# ---------- TEST 16 : Policy + Leave ----------
# test_cases = [
#     "Can I carry forward leave? Also take annual leave on 20 Aug."
# ]

# ---------- TEST 17 : Long Conversation ----------
test_cases = [
    "Hi",
    "Show my balance",
    "Show my leave history",
    "Can I carry forward annual leave?",
    "Take annual leave on 10 Sep.",
    "10 Sep.",
    "Actually make it two days.",
    "Show my balance.",
    "Cancel it.",
    "Show my leave history.",
    "Hi again.",
    "Take sick leave tomorrow.",
    "Tomorrow only.",
    "Actually change it to next Monday.",
    "Show my balance.",
    "Can I carry forward leave?",
    "Show my leave history."
]

# ============================================================

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