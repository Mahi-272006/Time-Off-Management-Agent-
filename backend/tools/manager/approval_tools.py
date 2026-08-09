import json

from langchain_core.tools import tool

from utils.paths import DATA_DIR

@tool
def approve_leave_request(request_id: int):
    """
    Approve a pending leave request.

    This tool is ONLY for managers.
    The planner must verify that the logged-in user is a manager
    before calling this tool.

    The request must exist and have status "Pending".
    """

    with open(DATA_DIR / "requests.json", "r") as f:
        requests = json.load(f)

    request = next(
        (r for r in requests if r["request_id"] == request_id),
        None
    )

    if request is None:
        return {
            "success": False,
            "message": "Leave request not found."
        }

    if request["status"] != "Pending":
        return {
            "success": False,
            "message": f"Cannot approve this request because its current status is {request['status']}."
        }

    request["status"] = "Approved"

    with open(DATA_DIR / "requests.json", "w") as f:
        json.dump(requests, f, indent=4)

    return {
        "success": True,
        "request_id": request_id,
        "status": "Approved",
        "message": "Leave request approved successfully."
    }


@tool
def reject_leave_request(request_id: int):
    """
    Reject a pending leave request.

    This tool is ONLY for managers.
    The planner must verify that the logged-in user is a manager
    before calling this tool.

    The request must exist and have status "Pending".
    """

    with open(DATA_DIR / "requests.json", "r") as f:
        requests = json.load(f)

    request = next(
        (r for r in requests if r["request_id"] == request_id),
        None
    )

    if request is None:
        return {
            "success": False,
            "message": "Leave request not found."
        }

    if request["status"] != "Pending":
        return {
            "success": False,
            "message": f"Cannot reject this request because its current status is {request['status']}."
        }

    request["status"] = "Rejected"

    with open(DATA_DIR / "requests.json", "w") as f:
        json.dump(requests, f, indent=4)

    return {
        "success": True,
        "request_id": request_id,
        "status": "Rejected",
        "message": "Leave request rejected successfully."
    }