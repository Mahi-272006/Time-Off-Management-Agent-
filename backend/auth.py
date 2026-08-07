import json
from pathlib import Path

EMPLOYEE_FILE = Path(__file__).parent / "data" / "employees.json"


def authenticate(employee_id: str, password: str):

    with open(EMPLOYEE_FILE, "r", encoding="utf-8") as f:
        employees = json.load(f)

    for employee in employees:

        if (
            employee["employee_id"] == employee_id
            and employee["password"] == password
        ):
            return employee

    return None