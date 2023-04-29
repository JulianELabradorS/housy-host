from firebase_admin import firestore
from flask import abort

from repositories.base_repository import get_firestore_client
import repositories.prorated_reservation_repository as prorated_reservation_repository
from models.reservation import get_reservation_object
from dateutil.relativedelta import relativedelta

firestore_client = get_firestore_client()


def save_reservations(reservations):
    try:
        batch = firestore_client.batch()
        collection = firestore_client.collection("reservations")
        for reservation in reservations:
            obj_reservation = get_reservation_object(reservation)
            tabulated_data = obj_reservation.get_prorated_data_of_reservation()
            prorated_reservation_repository.save_prorated_reservation(tabulated_data)
            batch.set(collection.document(str(obj_reservation.id)),
                      obj_reservation.to_dict())
            batch.commit()
        return "Batch saved"
    except Exception as e:
        return "ERROR. Batch not saved. Exception: %" % e


def create_reservation(reservation):
    obj_reservation = get_reservation_object(reservation)
    tabulated_data = obj_reservation.get_prorated_data_of_reservation()
    prorated_reservation_repository.update_prorated_reservation(tabulated_data)
    document = firestore_client.collection(
        "reservations").document(str(obj_reservation.id))
    document.set(obj_reservation.to_dict())
    return "Reservation saved"


def update_reservation(reservation):
    obj_reservation = get_reservation_object(reservation)
    tabulated_data = obj_reservation.get_prorated_data_of_reservation()
    prorated_reservation_repository.update_prorated_reservation(tabulated_data)
    document = firestore_client.collection(
        "reservations").document(str(obj_reservation.id))
    document.update(obj_reservation.to_dict())
    return document


def get_paginated_reservations(limit, start_at, propertyId, date):
    query = firestore_client.collection("reservations")
    reservations = []

    # Aplicar filtros iniciales
    query = query.where('status', 'in', ['new', 'modified']).order_by(
        'id', direction=firestore.Query.DESCENDING)
    if (date):
        query = query.where("arrivalDateMonth", "==", date.month).where(
            "arrivalDateYear", "==", date.year)
    if (propertyId):
        query = query.where('listingMapId', '==', int(propertyId))
    if (start_at):
        query = query.start_at({u'id': int(start_at)})
    query = query.limit(int(limit))
    result = query.get()
    print(result)
    for reservation in result:
        reservation_dict = reservation.to_dict()
        date_fields = ["reservationDate",
                       "arrivalDate",
                       "departureDate",
                       "previousArrivalDate",
                       "previousDepartureDate",
                       "cancellationDate",
                       "insertedOn",
                       "updatedOn",
                       "latestActivityOn"]
        for field in date_fields:
            if reservation_dict[field]:
                reservation_dict[field] = reservation_dict[field].strftime(
                    "%Y-%m-%d")
        reservations.append(reservation_dict)

    return {'data': reservations,
            'last_id': reservations[-1]["id"] if len(reservations) else None}


def update_fields_real_total_paid_in_reservation(id, currency, totalPaid, totalPaidCleaning):
    doc_ref = firestore_client.collection(
        "reservations").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        return 'there is no reservation with this id', 404
    doc_ref.update(
        {"realValueReceived": totalPaid, "realCleaningFee": totalPaidCleaning, "realValuesCurrency": currency})
    prorated_reservation_repository.update_real_totals_in_prorrated_reservations(
        id, currency, totalPaid, totalPaidCleaning)
    return {"sucess": True}
