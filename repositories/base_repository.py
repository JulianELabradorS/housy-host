import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./assets/cloudconsole.credentials.json")
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()


def get_firestore_client():
    return firestore_client
