from langchain_core.messages import HumanMessage
from graph import graph

state = {
    "messages": [],
    "employee_id": "EMP002",
    "employee": {
        "name": "Rahul",
        "country": "Germany",
        "department": "HR",
    },
    "tool_results": {},
    "retrieved_docs": [],
    "final_response": "",
    "needs_clarification": False,
    "clarification_question": "",
    "summary": "",
    "pending_leave": {
        "leave_type": None,
        "start_date": None,
        "end_date": None,
        "reason": None,
    },
}

print("=" * 70)
print("Acme Time-Off Agent")
print("Type 'exit' to quit.")
print("=" * 70)

while True:

    user_input = input("\nUSER: ")

    if user_input.lower() == "exit":
        break

    state["messages"].append(
        HumanMessage(content=user_input)
    )

    state = graph.invoke(state)

    print("\nBOT:")
    print(state["messages"][-1].content)

    print("\nCurrent Pending Leave State:")
    print(state["pending_leave"])

    print("\n" + "=" * 70)