import sys
import json
from pathlib import Path

# ---------------------------------------------------
# Add backend to Python path
# ---------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from graph import graph
from langchain_core.messages import HumanMessage


# ---------------------------------------------------
# Load Golden Dataset
# ---------------------------------------------------

dataset_path = (
    Path(__file__).parent
    / "golden_dataset.json"
)

with open(dataset_path, "r", encoding="utf-8") as f:
    golden_dataset = json.load(f)


results = []


# ---------------------------------------------------
# Run Every Test Case
# ---------------------------------------------------

for test in golden_dataset:

    print("=" * 70)
    print(f"Running Test {test['id']}")
    print(test["query"])
    print("=" * 70)

    state = {

        "messages": [
            HumanMessage(content=test["query"])
        ],

        # Logged-in employee
        "employee_id": "EMP002",

        "employee": None,

    }

    try:

        final_state = graph.invoke(state)

        response = final_state["messages"][-1].content

        # ---------------------------------------
        # Capture tool calls
        # ---------------------------------------

        tools_used = []

        for message in final_state["messages"]:

            if hasattr(message, "tool_calls"):

                if message.tool_calls:

                    for tool in message.tool_calls:

                        tools_used.append(tool["name"])

    except Exception as e:

        response = f"ERROR: {str(e)}"

        tools_used = []

    # ---------------------------------------
    # Save Result
    # ---------------------------------------

    results.append({

        "id": test["id"],

        "category": test["category"],

        "query": test["query"],

        "expected": test["expected"],

        "response": response,

        "tools_used": tools_used,

    })


# ---------------------------------------------------
# Save Results
# ---------------------------------------------------

reports_dir = (
    Path(__file__).parent
    / "reports"
)

reports_dir.mkdir(exist_ok=True)

output = (
    reports_dir
    / "evaluation_results.json"
)

with open(output, "w", encoding="utf-8") as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False,
    )


print("\n")
print("=" * 70)
print("Evaluation Completed Successfully")
print("=" * 70)
print(f"Executed {len(results)} test cases.")
print(f"Results saved to:\n{output}")