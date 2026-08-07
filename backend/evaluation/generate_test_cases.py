import sys
import json
from pathlib import Path

# ---------------------------------------------------
# Add backend folder to Python path
# ---------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from llm import llm
from langchain_core.messages import HumanMessage


# ---------------------------------------------------
# Prompt
# ---------------------------------------------------

prompt = """
Generate 50 realistic test cases for an AI Leave Management Assistant.

The assistant can:
- Check leave balance
- Explain leave policies
- Apply for leave
- Modify leave requests
- Cancel leave requests
- Show leave history
- Understand relative dates like today, tomorrow, next Monday, next Friday, next week
- Ask clarification questions when required
- Reject invalid leave requests

Generate exactly:

- 20 Happy Path queries
- 15 Ambiguous queries
- 10 Edge Case queries
- 5 Adversarial queries

For EACH test case return JSON in this EXACT format:

[
    {
        "id": 1,
        "category": "balance",
        "query": "How many annual leave days do I have left?",
        "expected": {
            "tool": "get_balance",
            "next_action": "respond",
            "contains": [
                "Annual Leave"
            ]
        }
    }
]

Allowed tool names ONLY:

- get_balance
- search_policy
- validate_leave_request
- modify_leave_request
- cancel_leave_request
- get_leave_requests
- null

Allowed next_action values ONLY:

- respond
- ask_clarification
- ask_confirmation
- reject

Guidelines:

- Queries must sound like real employees.
- Never mention APIs.
- Never mention tool names.
- Never mention employee IDs.
- Never mention JSON.
- Include policy questions.
- Include balance questions.
- Include leave application.
- Include leave modification.
- Include cancellation.
- Include leave history.
- Include relative dates.
- Include invalid dates.
- Include missing information.
- Include adversarial prompts.

Return ONLY valid JSON.

Do NOT wrap the JSON inside markdown.
Do NOT include explanations.
"""


# ---------------------------------------------------
# Invoke Claude
# ---------------------------------------------------

response = llm.invoke(
    [
        HumanMessage(content=prompt)
    ]
)

text = response.content.strip()


# ---------------------------------------------------
# Remove Markdown if Claude returns it
# ---------------------------------------------------

if text.startswith("```json"):
    text = text.replace("```json", "", 1)

if text.startswith("```"):
    text = text.replace("```", "", 1)

if text.endswith("```"):
    text = text[:-3]

text = text.strip()


# ---------------------------------------------------
# Parse JSON
# ---------------------------------------------------

try:

    test_cases = json.loads(text)

except json.JSONDecodeError:

    print("\nClaude returned invalid JSON:\n")
    print(text)
    raise


# ---------------------------------------------------
# Save File
# ---------------------------------------------------

output = (
    Path(__file__).parent
    / "generated_test_cases.json"
)

with open(output, "w", encoding="utf-8") as f:

    json.dump(
        test_cases,
        f,
        indent=4,
        ensure_ascii=False,
    )


print("\n========================================")
print(f"Generated {len(test_cases)} test cases.")
print(f"Saved to:\n{output}")
print("========================================")