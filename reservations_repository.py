import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./assets/firebase-credentials.json")
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()


def save_reservations(reservations):
    try:
        batch = firestore_client.batch()
        collection = firestore_client.collection("reservations")
        for reservation in reservations:
            batch.set(collection.document(str(reservation["id"])), reservation)
        batch.commit()
        return "Batch saved"
    except Exception as e:
        return "ERROR. Batch not saved. Exception: %" % e


def create_reservation(reservation):
    try:
        document = firestore_client.collection(
            "reservations").document(str(reservation['id']))
        document.set(reservation)

        return "Reservation saved"

    except Exception as e:
        return "ERROR. Reservation not saved. Exception %" % e


def update_reservation(reservation):
    try:
        document = firestore_client.collection(
            "reservations").document(str(reservation['id']))
        document.update(reservation)

        return "Reservation updated"
    except Exception as e:
        print(e)
        return create_reservation(reservation)
