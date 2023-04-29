import repositories.prorated_reservation_repository as prorated_reservation_repository


def get_prorated_reservations(limit, start_at, propertyId, date):
    return prorated_reservation_repository.get_prorated_reservations(limit, start_at, propertyId, date)


def get_prorated_by_reservation_id(reservationId):
    return prorated_reservation_repository.get_prorated_data_by_reservation_id(reservationId)
