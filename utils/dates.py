from datetime import datetime
from dateutil.relativedelta import relativedelta


def normalize_date(string_date: str) -> datetime or None:
    if (string_date):
        len_date_array = len(string_date.split(" "))
        if (len_date_array == 2):
            return datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")
        else:
            return datetime.strptime(string_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return None


def calculate_nights_by_month(check_in_date, check_out_date):
    check_in_month_start = datetime(check_in_date.year, check_in_date.month, 1)
    nights_in_first_month = min((check_in_month_start + relativedelta(
        months=1) - check_in_date).days, (check_out_date - check_in_date).days)

    result = {(check_in_date.year, check_in_date.month): nights_in_first_month}
    current_month = check_in_month_start + relativedelta(months=1)
    total_nights = nights_in_first_month

    while current_month < check_out_date:
        year_month_key = (current_month.year, current_month.month)
        days_in_month = (
            (current_month + relativedelta(months=1)) - current_month).days
        nights_in_month = min(
            (check_out_date - current_month).days, days_in_month)
        result[year_month_key] = nights_in_month
        total_nights += nights_in_month
        current_month = current_month + relativedelta(months=1)

    return [{"year": year, "month": month, "nights": nights} for (year, month), nights in result.items()], total_nights


def convert_to_first_day_of_month_iso_string(date: str) -> datetime:
    return datetime.fromisoformat(date.replace('Z', '+00:00')).replace(hour=0, minute=0, second=0, microsecond=0, day=1)


def convert_to_start_of_day_of_month_iso_string(date: str) -> datetime:
    return datetime.fromisoformat(date.replace('Z', '+00:00')).replace(hour=0, minute=0, second=0, microsecond=0)
