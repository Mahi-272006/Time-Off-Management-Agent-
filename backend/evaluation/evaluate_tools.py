import json
from pathlib import Path

# ---------------------------------------------------
# Load Evaluation Results
# ---------------------------------------------------

results_path = (
    Path(__file__).parent
    / "reports"
    / "evaluation_results.json"
)

with open(results_path, "r", encoding="utf-8") as f:
    results = json.load(f)

# ---------------------------------------------------
# Evaluate Tool Calls
# ---------------------------------------------------

passed = 0

print("=" * 70)
print("TOOL CALL ACCURACY EVALUATION")
print("=" * 70)

for test in results:

    expected_tool = test["expected"].get("tool")
    actual_tools = test.get("tools_used", [])

    # ------------------------------------------------
    # Cases where NO tool is expected
    # ------------------------------------------------

    if expected_tool is None or str(expected_tool).lower() == "null":

        # PASS only when the agent actually called no tool
        success = len(actual_tools) == 0

        if success:
            passed += 1

        test["tool_passed"] = success

        print(
            f"Test {test['id']:02d}"
            f" | Expected: None"
            f" | Actual: {actual_tools}"
            f" | {'PASS' if success else 'FAIL'}"
        )

        continue

    # ------------------------------------------------
    # Check whether expected tool was used
    # ------------------------------------------------

    success = expected_tool in actual_tools

    if success:
        passed += 1

    test["tool_passed"] = success

    print(
        f"Test {test['id']:02d}"
        f" | Expected: {expected_tool}"
        f" | Actual: {actual_tools}"
        f" | {'PASS' if success else 'FAIL'}"
    )

# ---------------------------------------------------
# Summary
# ---------------------------------------------------

evaluated = len(results)

accuracy = passed / evaluated if evaluated else 0

print("\n")
print("=" * 70)
print(
    f"Tool Call Accuracy : {accuracy:.2%}"
    f" ({passed}/{evaluated})"
)
print("=" * 70)

# ---------------------------------------------------
# Save Updated Results
# ---------------------------------------------------

with open(results_path, "w", encoding="utf-8") as f:
    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )