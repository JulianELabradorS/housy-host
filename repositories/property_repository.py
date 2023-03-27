
from models.property import Property
from repositories.base_repository import get_firestore_client

firestore_client = get_firestore_client()


def get_property(listingName: str) -> Property:
    document = firestore_client.collection(
        "properties").where(u'listingName', u'==', listingName).get()

    mockJson = {"listingName": listingName, "negotiations": [], "trms": []}

    return Property(document[0]._data) if len(document) != 0 else Property(mockJson)


def update_property(property):
    documentId = firestore_client.collection(
        "properties").where(u'listingName', u'==', property["listingName"]).get()

    document = firestore_client.collection(
        "properties").document(documentId[0].id)

    document.update(property)

    return "OK"


def get_properties():
    try:
        result = firestore_client.collection(
            "properties").get()

        return {"properties": [res._data["listingName"] for res in result]}
    except Exception as e:
        print(e)


def check_new_property(listingName):
    properties = get_properties()["properties"]

    if listingName in properties:
        return

    firestore_client.collection(
        "properties").add({"listingName": listingName})
