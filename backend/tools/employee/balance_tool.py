import json
from langchain_core.tools import tool
from utils.paths import DATA_DIR

@tool
def get_balance(employee_id: str) -> dict:
    """
    Retrieve the current leave balances for an employee.

    Use this tool whenever the user asks about:

    - Leave balance
    - PTO balance
    - Annual leave remaining
    - Sick leave balance
    - Remaining vacation days

    Input:
        employee_id: The employee's unique ID.

    Returns:
        Available leave balances for all leave types.

    Never guess leave balances.
    Always use this tool for balance-related questions.
    """

    try:
        with open(DATA_DIR / "balances.json", "r", encoding="utf-8") as f:
            balances = json.load(f)

    except FileNotFoundError:
        return {
            "error": "Leave balance database is unavailable. Please contact the administrator."
        }

    except json.JSONDecodeError:
        return {
            "error": "Leave balance database is corrupted. Please contact the administrator."
        }

    for balance in balances:
        if balance["employee_id"] == employee_id:
            return balance

    return {"error": "Balance not found"}