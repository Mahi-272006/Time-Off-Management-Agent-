from graph import graph
from langchain_core.messages import HumanMessage

state = {
    "messages": [],
    "employee_id": "EMP002",
}

print("=" * 70)
print("Acme Time-Off Agent")
print("Type 'exit' to quit.")
print("=" * 70)

while True:
    user = input("\nUSER: ")

    if user.lower() == "exit":
        break

    state["messages"].append(HumanMessage(content=user))

    state = graph.invoke(state)

    print("\nBOT:")
    print(state["messages"][-1].content)