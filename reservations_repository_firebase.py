import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from models.reservation import Reservation
from utils.dates import get_month, get_year

cred = credentials.Certificate("./assets/cloudconsole.credentials.json")
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()


def save_reservations(reservations):
    try:
        batch = firestore_client.batch()
        collection = firestore_client.collection("reservations")
        for reservation in reservations:
            reservation = complete_columns_data(reservation)
            batch.set(collection.document(str(reservation["id"])), reservation)
        batch.commit()
        return "Batch saved"
    except Exception as e:
        return "ERROR. Batch not saved. Exception: %" % e


def create_reservation(reservation):
    try:
        reservation = complete_columns_data(reservation)

        document = firestore_client.collection(
            "reservations").document(str(reservation['id']))
        document.set(reservation)

        return "Reservation saved"

    except Exception as e:
        return "ERROR. Reservation not saved. Exception %" % e
        # reservation["airbnbListingCleaningFee"] if reservation["channelName"] == "airbnbOfficial" else reservation["cleaningFee"],


def update_reservation(reservation):
    try:
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
        reservation["anio"]
    )


def complete_columns_data(reservation):
    reservation["aseoPpto"] = reservation["airbnbListingCleaningFee"] if reservation[
        "channelName"] == "airbnbOfficial" else reservation["cleaningFee"]
    reservation["aseoReal"] = reservation["aseoPpto"]
    reservation["mes"] = get_month(reservation["reservationDate"])
    reservation["anio"] = get_year(reservation["reservationDate"])

    return reservation
