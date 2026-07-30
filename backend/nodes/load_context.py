from tools.employee_tool import get_employee

def load_context_node(state):
    """
    Load employee details into the graph state.
    """

    employee = get_employee.invoke(
        {"employee_id": state["employee_id"]}
    )

    return {
        "employee": employee
    }