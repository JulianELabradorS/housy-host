import repositories.real_trm_repository as real_trm_repository
import repositories.prorated_reservation_repository as prorated_reservation_repository
from utils.dates import convert_to_start_of_day_of_month_iso_string
from datetime import datetime


def get_real_trm_by_year(year):
    return real_trm_repository.get_all_real_trm_added_by_year(int(year))


def create_real_trm(data):
    value = data.get("value")
    start_date = convert_to_start_of_day_of_month_iso_string(
        data.get("startDate"))
    end_date = convert_to_start_of_day_of_month_iso_string(
        data.get("endDate"))
    return real_trm_repository.create_real_trm(start_date, end_date, value)



def update_real_trm(id, data):
    value = data.get("value")
    start_date = convert_to_start_of_day_of_month_iso_string(
        data.get("startDate"))
    end_date = convert_to_start_of_day_of_month_iso_string(
        data.get("endDate"))
    return real_trm_repository.update_real_trm(id, value, start_date, end_date)
