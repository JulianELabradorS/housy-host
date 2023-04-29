
from models.property import Property
import repositories.reservations_repository as reservations_repository
import repositories.prorated_reservation_repository as prorated_reservation_repository


def create_reservation(reservation):
    return reservations_repository.create_reservation(reservation)


def update_reservation(reservation):
    return reservations_repository.update_reservation(reservation)


def get_paginated_reservations(limit, start_at, propertyId, date):
    return reservations_repository.get_paginated_reservations(limit, start_at, propertyId, date)


def update_fields_in_reservation(id, data):
    currency = data.get("currency")
    totalPaid = data.get("totalPaid")
    totalPaidCleaning = data.get("totalPaidCleaning")
    return reservations_repository.update_fields_real_total_paid_in_reservation(
        id, currency, totalPaid, totalPaidCleaning)
