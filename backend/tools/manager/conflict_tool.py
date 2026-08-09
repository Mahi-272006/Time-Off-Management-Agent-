import json

from langchain_core.tools import tool
from utils.paths import DATA_DIR


@tool
def detect_team_conflicts(employee_id: str):
    """
    Detect overlapping leave requests in the manager's team.

    Use this tool when a manager asks about:
    - Leave conflicts
    - Overlapping team leave
    - Staffing conflicts
    - Multiple employees on leave at the same time

    Only Pending and Approved requests are considered.

    The manager's own employee_id is used to identify the manager.
    """

    # --------------------------------------------------
    # Load employees
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Verify manager
    # --------------------------------------------------

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
            "message": "Manager not found."
        }

    if manager.get("role") != "manager":
        return {
            "success": False,
            "message": "This tool is only available to managers."
        }

    # --------------------------------------------------
    # Load leave requests
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Get active requests
    # --------------------------------------------------

    active_requests = [
        request
        for request in requests
        if request.get("status") in ["Pending", "Approved"]
    ]

    # --------------------------------------------------
    # Find overlapping requests
    # --------------------------------------------------

    conflicts = []

    for i in range(len(active_requests)):

        request_a = active_requests[i]

        for j in range(i + 1, len(active_requests)):

            request_b = active_requests[j]

            # Same employee is not a team conflict
            if request_a["employee_id"] == request_b["employee_id"]:
                continue

            start_a = request_a["start_date"]
            end_a = request_a["end_date"]

            start_b = request_b["start_date"]
            end_b = request_b["end_date"]

            # Date ranges overlap when:
            # A starts before B ends
            # AND
            # B starts before A ends

            if start_a <= end_b and start_b <= end_a:

                conflicts.append({
                    "request_1": request_a["request_id"],
                    "employee_1": request_a["employee_id"],
                    "leave_type_1": request_a["leave_type"],
                    "start_date_1": start_a,
                    "end_date_1": end_a,
                    "status_1": request_a["status"],

                    "request_2": request_b["request_id"],
                    "employee_2": request_b["employee_id"],
                    "leave_type_2": request_b["leave_type"],
                    "start_date_2": start_b,
                    "end_date_2": end_b,
                    "status_2": request_b["status"],
                })

    # --------------------------------------------------
    # No conflicts
    # --------------------------------------------------

    if not conflicts:
        return {
            "success": True,
            "conflicts_found": False,
            "count": 0,
            "message": "No overlapping team leave requests were found."
        }

    # --------------------------------------------------
    # Return conflicts
    # --------------------------------------------------

    return {
        "success": True,
        "conflicts_found": True,
        "count": len(conflicts),
        "conflicts": conflicts
    }