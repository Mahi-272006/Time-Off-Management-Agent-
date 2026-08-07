import json
import re
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from llm import llm
from langchain_core.messages import HumanMessage

# ---------------------------------------------------

results_path = (
    Path(__file__).parent
    / "reports"
    / "evaluation_results.json"
)

with open(results_path, "r", encoding="utf-8") as f:
    results = json.load(f)

# ---------------------------------------------------

prompt_template = """
You are an evaluation judge for an AI Leave Management Assistant.

Evaluate whether the assistant selected the CORRECT NEXT ACTION.

User Query:
{query}

Expected Next Action:
{expected}

Agent Response:
{response}

Possible next actions:

- respond
- ask_confirmation
- ask_clarification
- reject

Scoring

5
Exactly the correct next action.

4
Reasonable next action although another could also work.

3
Partially appropriate.

2
Poor workflow choice.

1
Completely wrong workflow.

Return ONLY JSON.

Example:

{{
    "score":5,
    "reasoning":"The assistant correctly asks for clarification before submitting."
}}
"""

print("=" * 70)
print("NEXT ACTION JUDGE")
print("=" * 70)

scores = []

for test in results:

    prompt = prompt_template.format(
        query=test["query"],
        expected=test["expected"]["next_action"],
        response=test["response"],
    )

    judge = llm.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    text = judge.content.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    try:
        verdict = json.loads(text)

    except Exception:

        verdict = {
            "score": 1,
            "reasoning": text
        }

    test["next_action_judge"] = verdict

    scores.append(verdict["score"])

    print(
        f"Test {test['id']:02d}"
        f" | Score: {verdict['score']}"
    )

average = sum(scores) / len(scores)

print("\n")
print("=" * 70)
print(f"Average Next Action Score : {average:.2f}/5")
print("=" * 70)

with open(results_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)