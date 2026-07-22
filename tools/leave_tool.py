import json
from datetime import datetime
from langchain_core.tools import tool


# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def calculate_days(start_date: str, end_date: str) -> int:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    return (end - start).days + 1


def check_balance(employee_id, leave_type, required_days):

    with open("data/balances.json", "r") as f:
        balances = json.load(f)

    balance = next(
        (b for b in balances if b["employee_id"] == employee_id),
        None
    )

    if balance is None:
        return False

    key = f"{leave_type.lower()}_leave"

    return balance.get(key, 0) >= required_days


def check_overlap(employee_id, start_date, end_date):

    with open("data/requests.json", "r") as f:
        requests = json.load(f)

    for req in requests:

        if req["employee_id"] != employee_id:
            continue

        if req["status"] == "Rejected":
            continue

        if not (
            end_date < req["start_date"]
            or start_date > req["end_date"]
        ):
            return True

    return False


def check_blackout(start_date, end_date):

    blackout_start = "2026-12-20"
    blackout_end = "2026-12-31"

    if not (
        end_date < blackout_start
        or start_date > blackout_end
    ):
        return True

    return False

@tool
def list_leave_requests(employee_id: str):
    """
    Retrieve the employee's leave request history.

    Use this tool whenever the user asks about:

    - Previous leave requests
    - Leave history
    - Pending requests
    - Approved requests
    - Rejected requests
    - Status of a leave request

    Input:
        employee_id: The employee's unique ID.

    Returns:
        A list of leave requests and their statuses.

    Never invent leave history.
    """

    with open("data/requests.json", "r") as f:
        requests = json.load(f)

    employee_requests = [
        req for req in requests
        if req["employee_id"] == employee_id
    ]

    if not employee_requests:
        return {
            "success": False,
            "message": "No leave requests found."
        }

    return {
        "success": True,
        "requests": employee_requests
    }


# ---------------------------------------------------
# Tool 2
# ---------------------------------------------------

@tool
def validate_leave_request(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
):
    """
    Validate a leave request before submission.

    Use this tool whenever an employee wants to apply
    for leave.

    This tool checks:

    - Leave balance
    - Leave eligibility
    - Blackout dates
    - Overlapping leave requests
    - Company leave rules

    Inputs:
        Employee ID
        Leave type
        Start date
        End date

    Returns:
        Whether the leave request is valid,
        along with the reason if validation fails.

    This tool DOES NOT submit the leave request.

    Always validate before submitting.
    """

    days = calculate_days(start_date, end_date)

    if days <= 0:
        return {
            "valid": False,
            "reason": "End date must be after start date.",
            "next_action": "stop"
        }

    if not check_balance(employee_id, leave_type, days):
        return {
            "valid": False,
            "reason": "Insufficient leave balance.",
            "next_action": "stop"
        }

    if check_overlap(employee_id, start_date, end_date):
        return {
            "valid": False,
            "reason": "Leave overlaps with an existing request.",
            "next_action": "stop"
        }

    if check_blackout(start_date, end_date):
        return {
            "valid": False,
            "reason": "Requested dates fall in a blackout period.",
            "next_action": "stop"
        }

    return {
        "valid": True,
        "days": days,
        "next_action": "submit"
    }

# ---------------------------------------------------
# Tool 3
# ---------------------------------------------------

@tool
def submit_leave_request(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
):
    """
    Submit a leave request after successful validation.

    Use this tool ONLY when:

    - validate_leave_request has already succeeded.

    Inputs:
        Employee ID
        Leave type
        Start date
        End date

    Returns:
        Confirmation that the leave request has been submitted.

    Never call this tool before validation.
    If validation fails, explain the failure instead of submitting.
    """

    with open("data/requests.json", "r") as f:
        requests = json.load(f)

    request = {
        "request_id": len(requests) + 1,
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "days": calculate_days(start_date, end_date),
        "status": "Pending"
    }

    requests.append(request)

    with open("data/requests.json", "w") as f:
        json.dump(requests, f, indent=4)

    return {
        "success": True,
        "request_id": request["request_id"],
        "status": "Pending"
    }