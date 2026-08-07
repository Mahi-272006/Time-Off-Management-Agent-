import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------
# Add backend to path
# ---------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from llm import llm
from langchain_core.messages import HumanMessage

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
# Judge Prompt
# ---------------------------------------------------

prompt_template = """
You are an evaluation judge for an AI Leave Management Assistant.

Evaluate ONLY the FAITHFULNESS of the response.

User Query:
{query}

Expected Behaviour:
{expected}

Agent Response:
{response}

Scoring Rubric

5:
Every factual claim is supported by the expected behaviour.

4:
Mostly faithful with one very minor unsupported statement.

3:
Mostly correct but contains one unsupported claim.

2:
Several unsupported or misleading claims.

1:
Hallucinates company policy, leave balance, employee data, or invents facts.

Return ONLY valid JSON.

Example:

{{
    "score":5,
    "reasoning":"The response is completely grounded."
}}
"""


# ---------------------------------------------------
# Run Judge
# ---------------------------------------------------

print("=" * 70)
print("FAITHFULNESS EVALUATION")
print("=" * 70)

scores = []

for test in results:

    prompt = prompt_template.format(
        query=test["query"],
        expected=json.dumps(test["expected"], indent=2),
        response=test["response"],
    )

    judge = llm.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    text = judge.content.strip()

    # Remove markdown if Claude adds it
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

    test["faithfulness"] = verdict

    scores.append(verdict["score"])

    print(
        f"Test {test['id']:02d}"
        f" | Score: {verdict['score']}"
    )


# ---------------------------------------------------
# Average
# ---------------------------------------------------

average = sum(scores) / len(scores)

print("\n")
print("=" * 70)
print(f"Average Faithfulness : {average:.2f}/5")
print("=" * 70)


# ---------------------------------------------------
# Save
# ---------------------------------------------------

with open(results_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)