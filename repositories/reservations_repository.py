from firebase_admin import firestore
from models.property import Property
from repositories.base_repository import get_firestore_client
from repositories.property_repository import check_new_property, get_property
from utils.columns_calculation import (
    calculate_columns_new_reservation,
    complete_calculated_columns_of_negotiation, complete_columns_data,
    get_reservation_object, transform_to_COP)

firestore_client = get_firestore_client()


def save_reservations(reservations):
    try:
        batch = firestore_client.batch()
        collection = firestore_client.collection("reservations")
        for reservation in reservations:
            batch.set(collection.document(str(reservation["id"])), reservation)

            check_new_property(reservation["listingName"])

        batch.commit()
        return "Batch saved"
    except Exception as e:
        return "ERROR. Batch not saved. Exception: %" % e


def create_reservation(reservation):
    try:
        reservation = complete_columns_data(reservation)
        reservation = calculate_columns_new_reservation(reservation)

        document = firestore_client.collection(
            "reservations").document(str(reservation['id']))
        document.set(reservation)

        check_new_property(reservation["listingName"])

        return "Reservation saved"

    except Exception as e:
        return "ERROR. Reservation not saved. Exception %" % e


def update_reservation(reservation):
    try:
        property = get_property(reservation["listingName"])
        reservation = update_computed_values(property)

        document = firestore_client.collection(
            "reservations").document(str(reservation['id']))
        document.update(reservation)

        return "Reservation updated"
    except Exception as e:
        print(e)
        return create_reservation(reservation)


def get_reservations():
    try:
        reservations = []
        result = firestore_client.collection("reservations").get()
        for res in result:
            reservations.append(get_reservation_object(res._data))

        return reservations
    except Exception as e:
        print(e)


def get_paginated_reservations(limit, start_at, order_by, direction):
    direction = firestore.Query.DESCENDING if direction == "descending" else firestore.Query.ASCENDING

    try:
        reservations = []

        if (start_at):
            query = firestore_client.collection(
                "reservations").order_by(order_by, direction=direction).start_at({u'id': int(start_at)}).limit(int(limit))
        else:
            query = firestore_client.collection(
                "reservations").order_by(order_by, direction=direction).limit(int(limit))

        result = query.get()

        for res in result:
            reservations.append(get_reservation_object(res._data))

        return {'reservations': [obj.__dict__ for obj in reservations],
                'last_id': reservations[-1].id}
    except Exception as e:
        print(e)


def update_computed_values_of_negotiation(property: Property):
    if (len(property.negotiations) == 0):
        return

    lastNegotiation = property.negotiations[-1]

    fileteredReservations = firestore_client.collection(
        "reservations").where(u'listingName', u'==', property.listingName).where(u'anio', u'>=', lastNegotiation.fromYear).where(u'anio', u'<=', lastNegotiation.toYear).get()

    for res in fileteredReservations:
        jsonReservation = res._data
        if (jsonReservation["monthNumber"] >= lastNegotiation.fromMonth
                & jsonReservation["monthNumber"] <= lastNegotiation.toMonth):
            jsonReservation["negotiation"] = lastNegotiation.percentage

            update_reservation(
                complete_calculated_columns_of_negotiation(jsonReservation), False)


def update_computed_values_of_trm(property: Property):
    if (len(property.trms) == 0):
        return

    lastTrm = property.trms[-1]

    fileteredReservations = firestore_client.collection(
        "reservations").where(u'listingName', u'==', property.listingName).where(u'anio', u'>=', lastTrm.fromYear).where(u'anio', u'<=', lastTrm.toYear).get()

    for res in fileteredReservations:
        jsonReservation = res._data
        if (jsonReservation["monthNumber"] >= lastTrm.fromMonth
                & jsonReservation["monthNumber"] <= lastTrm.toMonth):
            jsonReservation["trm"] = lastTrm.trm
            update_reservation(
                transform_to_COP(jsonReservation), False)


def update_computed_values(property: Property):
    update_computed_values_of_trm(property)
    update_computed_values_of_negotiation(property)
