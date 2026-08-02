import json
from utils.paths import DATA_DIR

def load_context_node(state):

    try:
        with open(DATA_DIR / "employees.json", "r") as f:
            employees = json.load(f)

    except FileNotFoundError:
        return {
            "employee": None,
            "error": "Employee database is unavailable. Please contact the administrator."
        }

    employee = next(
        (
            e
            for e in employees
            if e["employee_id"] == state["employee_id"]
        ),
        None,
    )

    if employee is None:
        return {
            "employee": None,
            "error": "Employee not found."
        }

    return {
        "employee": employee
    }