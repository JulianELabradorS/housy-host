import firebase_admin
from firebase_admin import credentials, firestore
from models.property import Property
from models.reservation import Reservation
from utils.dates import get_month, get_month_str, get_year

cred = credentials.Certificate("./assets/cloudconsole.credentials.json")
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()


def save_reservations(reservations):
    try:
        batch = firestore_client.batch()
        collection = firestore_client.collection("reservations")
        for reservation in reservations:
            reservation = complete_columns_data(reservation)
            reservation = calculate_columns_new_reservation(reservation)

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


def get_reservation_object(reservation) -> Reservation:
    return Reservation(
        reservation["id"],
        reservation["guestName"],
        reservation["totalPrice"],
        reservation["aseoPpto"],
        reservation["comisionPpto"] if "comisionPpto" in reservation else "",
        reservation["comisionReal"] if "comisionReal" in reservation else "",
        reservation["netoPropietario"] if "netoPropietario" in reservation else "",
        reservation["presupuestoReal"] if "presupuestoReal" in reservation else "",
        reservation["aseoReal"] if "aseoReal" in reservation else "",
        reservation["nights"],
        reservation["channelName"],
        reservation["negociacion"] if "negociacion" in reservation else "",
        reservation["mes"],
        reservation["anio"],
        reservation["listingName"],
        reservation["currency"],
        reservation["trm"] if "trm" in reservation else "",
        reservation["cop"] if "cop" in reservation else "",
    )


def complete_columns_data(reservation):
    reservation["aseoPpto"] = reservation["airbnbListingCleaningFee"] if reservation[
        "channelName"] == "airbnbOfficial" else reservation["cleaningFee"]
    reservation["aseoReal"] = reservation["aseoPpto"]
    reservation["mes"] = get_month_str(reservation["reservationDate"])
    reservation["monthNumber"] = get_month(reservation["reservationDate"])
    reservation["anio"] = get_year(reservation["reservationDate"])

    return reservation


def calculate_columns_new_reservation(reservation):
    reservation['trm'] = get_property_last_trm(reservation["listingName"])
    reservation['negotiation'] = get_property_last_negotiation(
        reservation["listingName"])

    reservation = complete_calculated_columns_of_trm(reservation)
    reservation = complete_calculated_columns_of_negotiation(reservation)

    return reservation


def complete_calculated_columns_of_negotiation(reservation):
    negotiationPercentage = int(reservation["negotiation"])
    reservation["comisionPpto"] = negotiationPercentage * \
        int(reservation["totalPrice"])

    if ("presupuestoReal" in reservation):
        reservation["comisionReal"] = negotiationPercentage * \
            (int(reservation["presupuestoReal"]) -
             int(reservation["aseoReal"]))

        reservation["netoPropietario"] = int(reservation["presupuestoReal"]) - \
            int(reservation["comisionReal"])

    return reservation


def complete_calculated_columns_of_trm(reservation):
    trm = reservation["trm"]

    if (reservation["currency"] != "COP"):
        reservation["cop"] = int(reservation["totalPrice"]) * int(trm)

    return reservation


def get_properties():
    try:
        result = firestore_client.collection(
            "properties").get()

        return {"properties": [res._data["listingName"] for res in result]}
    except Exception as e:
        print(e)


def check_new_property(listingName):
    result = firestore_client.collection(
        "properties").get()

    properties = [res._data["listingName"] for res in result]

    if listingName in properties:
        return

    firestore_client.collection(
        "properties").add({"listingName": listingName})


def update_computed_values(property: Property):
    update_computed_values_of_trm(property)
    update_computed_values_of_negotiation(property)


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
                complete_calculated_columns_of_trm(jsonReservation), False)


def get_property(listingName: str) -> Property:
    document = firestore_client.collection(
        "properties").where(u'listingName', u'==', property["listingName"]).get()

    mockJson = {"listingName": listingName, "negotiations": [], "trms": []}

    Property(document[0]._data) if len(document) != 0 else Property(mockJson)


def update_property(property):
    documentId = firestore_client.collection(
        "properties").where(u'listingName', u'==', property["listingName"]).get()

    document = firestore_client.collection(
        "properties").document(documentId[0].id)

    document.update(property)

    update_computed_values(Property(property))

    return "OK"


def get_property_last_trm(listingName: str):
    property = get_property(listingName)

    if (len(property.trms) == 0):
        return 4700

    return property.trms[-1].trm


def get_property_last_negotiation(listingName: str):
    property = get_property(listingName)

    if (len(property.negotiations) == 0):
        return 0.2

    return property.negotiations[-1].percentage
