MANAGER_TOOLS = {
    "get_pending_team_leave_requests",
    "approve_leave_request",
    "reject_leave_request",
    "detect_team_conflicts",
}


def is_tool_authorized(tool_name: str, role: str) -> bool:

    # Manager tools require manager role
    if tool_name in MANAGER_TOOLS:
        return role == "manager"

    # Employee tools are available to employees and managers
    return True