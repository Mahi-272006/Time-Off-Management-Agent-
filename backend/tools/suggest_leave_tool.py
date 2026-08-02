import json
from datetime import datetime, timedelta

from langchain_core.tools import tool

from utils.paths import DATA_DIR
from tools.validation_leave_request_logic import (
    get_date_range,
    check_holiday,
    get_employee_country,
)

@tool
def suggest_leave_dates(
    employee_id: str,
    month: int,
    year: int,
):
    """
    Suggest leave dates that maximize consecutive days off.

    Use ONLY when the employee asks for recommendations like:

    - Suggest vacation
    - Recommend leave dates
    - Best time to take leave
    - Long weekend
    """

    country = get_employee_country(employee_id)

    suggestions = []

    first_day = datetime(year, month, 1).date()

    if month == 12:
        last_day = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1).date() - timedelta(days=1)

    current = first_day

    while current <= last_day:

        if current.weekday() < 5:

            holiday = check_holiday(str(current), country)

            if holiday["success"] and holiday["is_holiday"]:

                prev = current - timedelta(days=1)
                nxt = current + timedelta(days=1)

                if prev.weekday() >= 5 or nxt.weekday() >= 5:

                    suggestions.append(
                        {
                            "holiday": holiday["holiday_name"],
                            "leave_date": str(current),
                            "reason": "Public holiday next to weekend"
                        }
                    )

        current += timedelta(days=1)

    return suggestions