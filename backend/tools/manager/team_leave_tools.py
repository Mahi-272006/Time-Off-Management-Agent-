import json

from langchain_core.tools import tool
from utils.paths import DATA_DIR
# ---------------------------------------------------
# Manager Tool 1
# ---------------------------------------------------

@tool
def get_pending_team_leave_requests(employee_id: str):
    """
    Get pending leave requests for the manager's team.

    Use this tool when a manager asks about:
    - Pending team leave
    - Team leave requests
    - Employees waiting for leave approval
    """

    # -----------------------------------------------
    # Load employees
    # -----------------------------------------------

    try:
        with open(DATA_DIR / "employees.json", "r", encoding="utf-8") as f:
            employees = json.load(f)

    except FileNotFoundError:
        return {
            "success": False,
            "message": "Employee database is unavailable."
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "Employee database is corrupted."
        }

    # -----------------------------------------------
    # Find the manager
    # -----------------------------------------------

    manager = next(
        (
            employee
            for employee in employees
            if employee["employee_id"] == employee_id
        ),
        None
    )

    if manager is None:
        return {
            "success": False,
            "message": "Employee not found."
        }

    # -----------------------------------------------
    # Permission check
    # -----------------------------------------------

    if manager.get("role") != "manager":
        return {
            "success": False,
            "message": "Manager permission required."
        }

    # -----------------------------------------------
    # Find manager's team
    # -----------------------------------------------

    team_members = [
        employee
        for employee in employees
        if employee.get("department") == manager.get("department")
        and employee.get("role") != "manager"
    ]

    team_employee_ids = {
        employee["employee_id"]
        for employee in team_members
    }

    # -----------------------------------------------
    # Load leave requests
    # -----------------------------------------------

    try:
        with open(DATA_DIR / "requests.json", "r", encoding="utf-8") as f:
            requests = json.load(f)

    except FileNotFoundError:
        return {
            "success": False,
            "message": "Leave request database is unavailable."
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "Leave request database is corrupted."
        }

    # -----------------------------------------------
    # Get pending team requests
    # -----------------------------------------------

    pending_requests = [
        request
        for request in requests
        if request.get("employee_id") in team_employee_ids
        and request.get("status") == "Pending"
    ]

    # -----------------------------------------------
    # No pending requests
    # -----------------------------------------------

    if not pending_requests:
        return {
            "success": True,
            "message": "There are no pending leave requests for your team.",
            "requests": []
        }

    # -----------------------------------------------
    # Add employee names
    # -----------------------------------------------

    employee_lookup = {
        employee["employee_id"]: employee["name"]
        for employee in team_members
    }

    results = []

    for request in pending_requests:

        results.append({
            **request,
            "employee_name": employee_lookup.get(
                request["employee_id"],
                request["employee_id"]
            )
        })

    return {
        "success": True,
        "requests": results
    }

