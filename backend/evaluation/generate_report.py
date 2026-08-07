import json
from pathlib import Path

results_path = (
    Path(__file__).parent
    / "reports"
    / "evaluation_results.json"
)

with open(results_path, "r", encoding="utf-8") as f:
    results = json.load(f)

total = len(results)

# ----------------------------
# Tool Accuracy
# ----------------------------

tool_correct = sum(
    test.get("passed", False)
    for test in results
)

tool_accuracy = tool_correct / total

# ----------------------------
# Workflow Accuracy
# ----------------------------

workflow_correct = sum(
    test.get("next_action_passed", False)
    for test in results
)

workflow_accuracy = workflow_correct / total

# ----------------------------
# Faithfulness
# ----------------------------

faith_scores = [
    test["faithfulness"]["score"]
    for test in results
    if "faithfulness" in test
]

faithfulness = (
    sum(faith_scores) / len(faith_scores)
    if faith_scores else 0
)

# ----------------------------
# Clarification
# ----------------------------

clarification_scores = [
    test["clarification_score"]["score"]
    for test in results
    if "clarification_score" in test
]

clarification = (
    sum(clarification_scores)
    / len(clarification_scores)
    if clarification_scores else 0
)

print("\n")
print("=" * 65)
print("TIME-OFF AGENT EVALUATION REPORT")
print("=" * 65)

print(f"Tool Accuracy          : {tool_accuracy:.2%}")

print(f"Workflow Accuracy      : {workflow_accuracy:.2%}")

print(f"Faithfulness           : {faithfulness:.2f}/5")

print(f"Clarification Quality  : {clarification:.2f}/5")

print("=" * 65)