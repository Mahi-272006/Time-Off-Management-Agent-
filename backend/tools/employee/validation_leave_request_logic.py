import json
from datetime import datetime, timedelta

import holidays

from utils.paths import DATA_DIR


# ======================================================
# Helper Functions
# ======================================================
def get_date_range(start_date: str, end_date: str):
    """
    Returns every date between start_date and end_date (inclusive).
    """

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    dates = []

    current = start

    while current <= end:
        dates.append(current)
        current += timedelta(days=1)

    return dates

def calculate_days(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1


def get_employee_country(employee_id):

    try:
        with open(DATA_DIR / "employees.json", "r") as f:
            employees = json.load(f)

    except FileNotFoundError:
        return {
            "success": False,
            "reason": "Employee records are temporarily unavailable."
        }
    
    employee = next(
        (e for e in employees if e["employee_id"] == employee_id),
        None
    )

    if employee is None:
        return {
            "success": False,
            "reason": "Employee not found."
        }

    return {
        "success": True,
        "country": employee["country"]
    }



def check_calendar(date_text: str):
    """
    Returns calendar information about the given date.
    """

    try:
        date = datetime.strptime(date_text, "%Y-%m-%d").date()

    except ValueError:

        return {
            "success": False,
            "reason": "Invalid date format."
        }

    today = datetime.today().date()
    print("TODAY =", today)
    print("INPUT =", date)
    return {
        "success": True,
        "date": str(date),
        "weekday": date.strftime("%A"),
        "is_today": date == today,
        "is_past": date < today,
        "is_weekend": date.weekday() >= 5
    }


def check_holiday(date: str, country: str):
    """
    Checks whether a date is a national/public holiday.
    """

    try:
        holiday_calendar = holidays.country_holidays(country)

    except Exception:

        return {
            "success": False,
            "reason": "Unsupported country."
        }

    if date in holiday_calendar:

        return {
            "success": True,
            "is_holiday": True,
            "holiday_name": holiday_calendar.get(date)
        }

    return {
        "success": True,
        "is_holiday": False,
        "holiday_name": None
    }


def check_balance(employee_id, leave_type, required_days):

    with open(DATA_DIR / "balances.json", "r") as f:
        balances = json.load(f)

    balance = next(
        (b for b in balances if b["employee_id"] == employee_id),
        None
    )

    if balance is None:
        return False

    key = leave_type.lower().replace(" ", "_")

    return balance.get(key, 0) >= required_days


def check_overlap(employee_id, start_date, end_date, ignore_request_id):

    with open(DATA_DIR / "requests.json", "r") as f:
        requests = json.load(f)

    for req in requests:

        if req["employee_id"] != employee_id:
            continue

        if ignore_request_id is not None and req["request_id"] == ignore_request_id:
            continue

        if req["status"] in ("Rejected", "Cancelled"):
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

    return not (
        end_date < blackout_start
        or start_date > blackout_end
    )


# ======================================================
# Individual Validators
# ======================================================

def validate_calendar(start_date):

    calendar = check_calendar(start_date)

    if not calendar["success"]:

        return {
            "valid": False,
            "reason": calendar["reason"],
            "next_action": "stop"
        }

    if calendar["is_past"]:

        return {
            "valid": False,
            "reason": "The selected date is in the past. Please choose today or a future date.",
            "next_action": "stop"
        }

    if calendar["is_weekend"]:

        return {
            "valid": False,
            "reason": f"{calendar['weekday']} is a weekend. You already have a day off, so no leave request is needed.",
            "next_action": "stop"
        }

    return {"valid": True}


def validate_holiday(start_date, country):

    holiday = check_holiday(start_date, country)

    if not holiday["success"]:

        return {
            "valid": False,
            "reason": holiday["reason"],
            "next_action": "stop"
        }

    if holiday["is_holiday"]:

        return {
            "valid": False,
            "reason": f"{holiday['holiday_name']} is already a public holiday. No leave request is required.",
            "next_action": "stop"
        }

    return {"valid": True}


def validate_balance(employee_id, leave_type, days):

    if not check_balance(employee_id, leave_type, days):

        return {
            "valid": False,
            "reason": "Insufficient leave balance.",
            "next_action": "stop"
        }

    return {"valid": True}


def validate_overlap(
    employee_id,
    start_date,
    end_date,
    ignore_request_id,
):

    if check_overlap(
        employee_id,
        start_date,
        end_date,
        ignore_request_id,
    ):

        return {
            "valid": False,
            "reason": "Leave overlaps with an existing request.",
            "next_action": "stop"
        }

    return {"valid": True}


def validate_blackout(start_date, end_date):

    if check_blackout(start_date, end_date):

        return {
            "valid": False,
            "reason": "Requested dates fall in a blackout period.",
            "next_action": "stop"
        }

    return {"valid": True}


# ======================================================
# Main Validation Pipeline
# ======================================================

def validate_leave_request_logic(
    employee_id,
    leave_type,
    start_date,
    end_date,
    ignore_request_id=None,
):

    print("\n========== VALIDATION ==========")
    print("Employee :", employee_id)
    print("Leave    :", leave_type)
    print("Start    :", start_date)
    print("End      :", end_date)

    days = calculate_days(start_date, end_date)

    dates = get_date_range(start_date, end_date)

    print("\nDates in request:")

    for d in dates:
        print(d)

    if days <= 0:

        return {
            "valid": False,
            "reason": "End date must be after start date.",
            "next_action": "stop"
        }

    country_result = get_employee_country(employee_id)

    if not country_result["success"]:
        return {
        "valid": False,
        "reason": country_result["reason"],
        "next_action": "stop"
        }

    country = country_result["country"]
    
    validators = [

        ("Calendar", lambda: validate_calendar(start_date)),

        ("Holiday", lambda: validate_holiday(
            start_date,
            country
        )),

        ("Balance", lambda: validate_balance(
            employee_id,
            leave_type,
            days
        )),

        ("Overlap", lambda: validate_overlap(
            employee_id,
            start_date,
            end_date,
            ignore_request_id
        )),

        ("Blackout", lambda: validate_blackout(
            start_date,
            end_date
        ))
    ]

    for name, validator in validators:

        print(f"\nRunning {name} validation...")

        result = validator()

        if result["valid"]:

            print(f"✓ {name} Passed")

        else:

            print(f"✗ {name} Failed")
            print(result["reason"])

            return result

    print("\n✓ All validations passed")

    return {
        "valid": True,
        "days": days,
        "next_action": "submit"
    }