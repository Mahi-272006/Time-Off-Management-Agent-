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
# Paths
# ---------------------------------------------------

EVALUATION_DIR = Path(__file__).parent

results_path = (
    EVALUATION_DIR
    / "reports"
    / "evaluation_results.json"
)

DATA_DIR = BACKEND_DIR / "data"


# ---------------------------------------------------
# Load Source Documents
# ---------------------------------------------------

def load_source_data():

    sources = {}

    # -----------------------------------------------
    # JSON data
    # -----------------------------------------------

    json_files = [
        "balances.json",
        "employees.json",
        "requests.json",
    ]

    for filename in json_files:

        path = DATA_DIR / filename

        if path.exists():

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                sources[filename] = json.load(f)

    # -----------------------------------------------
    # Policy documents
    # -----------------------------------------------

    policies_dir = DATA_DIR / "policies"

    if policies_dir.exists():

        for path in policies_dir.glob("*.md"):

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                sources[f"policies/{path.name}"] = f.read()

    return sources


# ---------------------------------------------------
# Load Evaluation Results
# ---------------------------------------------------

with open(results_path, "r", encoding="utf-8") as f:

    results = json.load(f)


# ---------------------------------------------------
# Load Source Data
# ---------------------------------------------------

source_data = load_source_data()


print("=" * 70)
print("FAITHFULNESS EVALUATION")
print("=" * 70)


# ---------------------------------------------------
# Judge Prompt
# ---------------------------------------------------

prompt_template = """
You are an evaluation judge for an AI Leave Management Assistant.

Evaluate ONLY the FAITHFULNESS of the assistant response.

Your job is to determine whether the factual claims made by the
assistant are supported by the available evidence.

You have access to:

1. The user query
2. The expected behaviour
3. The actual assistant response
4. The actual tools used
5. The actual tool outputs
6. The underlying source documents and demo data

IMPORTANT RULES:

- The expected behaviour describes what the agent should do.
- The expected behaviour does NOT necessarily contain every factual
  value that the assistant is allowed to return.
- If a factual claim is supported by an actual tool output,
  consider that claim grounded.
- If a factual claim is supported by the provided source documents,
  consider that claim grounded.
- Do NOT mark a claim as hallucinated merely because that exact value
  does not appear in the expected behaviour.
- For employee balances, leave requests, dates, request IDs, etc.,
  use the actual tool output and source data as the source of truth.
- For company policies, use the provided policy documents and tool
  outputs as the source of truth.
- Do not assume that a claim is false merely because the expected
  behaviour does not mention it.
- Penalize the assistant only when a factual claim is unsupported,
  contradictory, fabricated, or misleading.
- Do not penalize normal conversational wording.

---------------------------------------------------
USER QUERY
---------------------------------------------------

{query}

---------------------------------------------------
EXPECTED BEHAVIOUR
---------------------------------------------------

{expected}

---------------------------------------------------
TOOLS USED
---------------------------------------------------

{tools_used}

---------------------------------------------------
ACTUAL TOOL OUTPUTS
---------------------------------------------------

{tool_outputs}

---------------------------------------------------
SOURCE DOCUMENTS / DEMO DATA
---------------------------------------------------

{source_data}

---------------------------------------------------
ASSISTANT RESPONSE
---------------------------------------------------

{response}

---------------------------------------------------
SCORING RUBRIC
---------------------------------------------------

5:
The response is fully grounded in the available evidence.
All important factual claims are supported by tool outputs or
source documents. No meaningful hallucinations.

4:
The response is strongly grounded but contains one very minor
unsupported statement that does not materially affect the answer.

3:
The response is mostly grounded but contains one meaningful
unsupported factual claim.

2:
The response contains several unsupported, misleading, or
contradictory factual claims.

1:
The response substantially hallucinates, fabricates employee data,
leave information, policy, tool results, or other important facts.

IMPORTANT:
Do not use the expected behaviour alone to determine factual
grounding. Use the actual tool outputs and source documents.

Return ONLY valid JSON.

Example:

{{
    "score": 5,
    "reasoning": "The response is fully grounded in the provided tool output."
}}
"""


# ---------------------------------------------------
# Run Judge
# ---------------------------------------------------

scores = []


for test in results:

    prompt = prompt_template.format(

        query=test["query"],

        expected=json.dumps(
            test["expected"],
            indent=2
        ),

        tools_used=json.dumps(
            test.get("tools_used", []),
            indent=2
        ),

        tool_outputs=json.dumps(
            test.get("tool_outputs", []),
            indent=2
        ),

        source_data=json.dumps(
            source_data,
            indent=2,
            ensure_ascii=False
        ),

        response=test["response"],
    )

    judge = llm.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    text = judge.content.strip()

    # -----------------------------------------------
    # Remove markdown code fences
    # -----------------------------------------------

    text = re.sub(
        r"^```json",
        "",
        text
    )

    text = re.sub(
        r"```$",
        "",
        text
    )

    text = text.strip()

    # -----------------------------------------------
    # Parse JSON
    # -----------------------------------------------

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

if scores:

    average = sum(scores) / len(scores)

else:

    average = 0


print("\n")
print("=" * 70)
print(
    f"Average Faithfulness : {average:.2f}/5"
)
print("=" * 70)


# ---------------------------------------------------
# Save
# ---------------------------------------------------

with open(
    results_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )