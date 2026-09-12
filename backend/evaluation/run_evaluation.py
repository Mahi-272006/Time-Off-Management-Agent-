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
        "employee_id": "EMP001",

        "employee": None,
    }

    try:

        final_state = graph.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": f"employee_test_{test['id']}"
                }
            }
        )

        response = final_state["messages"][-1].content

        # ---------------------------------------
        # Capture tool calls
        # ---------------------------------------

        tools_used = []

        # ---------------------------------------
        # Capture actual tool outputs
        # ---------------------------------------

        tool_outputs = []

        for message in final_state["messages"]:

            # Tool calls made by the LLM
            if hasattr(message, "tool_calls"):

                if message.tool_calls:

                    for tool in message.tool_calls:

                        tools_used.append(tool["name"])

            # Tool results
            #
            # ToolMessage normally has:
            # - name
            # - content
            # - tool_call_id
            #
            if hasattr(message, "tool_call_id"):

                tool_outputs.append({
                    "tool": getattr(message, "name", None),
                    "tool_call_id": message.tool_call_id,
                    "output": message.content,
                })

    except Exception as e:

        response = f"ERROR: {str(e)}"

        tools_used = []

        tool_outputs = []

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

        "tool_outputs": tool_outputs,

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