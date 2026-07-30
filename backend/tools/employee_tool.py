import json
from langchain_core.tools import tool
from utils.paths import DATA_DIR

@tool
def get_employee(employee_id: str) -> dict:
    """
    Retrieve the profile information of an employee.

    Use this tool when employee details are required,
    such as name, country, department, manager,
    or other profile information.

    Input:
        employee_id: The employee's unique ID.

    Returns:
        The employee's profile information.

    Do not use this tool for leave balances,
    leave requests, or company policy questions.
    """

    with open(DATA_DIR / "employees.json", "r") as f:
        employees = json.load(f)

    for employee in employees:
        if employee["employee_id"] == employee_id:
            return employee

    return {"error": "Employee not found"}