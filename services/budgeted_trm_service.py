import repositories.budgeted_trm_repository as budgeted_trm_repository
from datetime import datetime
from utils.dates import convert_to_first_day_of_month_iso_string


def get_all_budgeted_trm_of_year(year):
    return budgeted_trm_repository.get_all_budgeted_trm_by_year(year)


def get_budgeted_trm(start_date):
    month = datetime.fromisoformat(start_date.replace('Z', '+00:00')).month
    return budgeted_trm_repository.get_budgeted_trm_of_month(month)


def create_budgeted_trm(data):
    value = data.get("value")
    date = convert_to_first_day_of_month_iso_string(data.get("date"))
    return budgeted_trm_repository.create_budgeted_trm(date, value)


def update_budgeted_trm(id, data):
    value = data.get("value")
    return budgeted_trm_repository.update_budgeted_trm(id, value)

