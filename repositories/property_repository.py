
from models.property import Property
from repositories.base_repository import get_firestore_client
from models.property import get_property_object
import repositories.prorated_reservation_repository as prorated_reservation_repository

firestore_client = get_firestore_client()


def save_properties(properties):
    try:
        batch = firestore_client.batch()
        collection = firestore_client.collection("properties")
        for property in properties:
            obj_property = get_property_object(property)
            batch.set(collection.document(str(obj_property.id)),
                      obj_property.to_dict())
            batch.commit()
        return "Batch saved"
    except Exception as e:
        return "ERROR. Batch not saved. Exception: %" % e


def get_all_properties():
    result = firestore_client.collection(
        "properties").get()
    doc_list = [doc.to_dict() for doc in result]
    return {"data": doc_list}


def update_property_percentage_negociated(id, percentage):
    doc_ref = firestore_client.collection(
        "properties").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        return 'there is no property with this id', 404
    doc_ref.update(
        {"percentageNegotiated": percentage,"isNew":False})
    property =doc.to_dict()
    if property["isNew"]:
        prorated_reservation_repository.update_property_percentage_in_proprrated_reservations(
            id, percentage)
    return {"success": True}


def get_property(propertyId: str) -> Property:
    doc_ref = firestore_client.collection("properties").document(propertyId)
    doc_data = doc_ref.get().to_dict()
    return {'data': doc_data}


def get_property_commission_percentage(propertyId: int) -> Property:
    doc_ref = firestore_client.collection(
        "properties").document(str(propertyId))
    doc_data = doc_ref.get().to_dict()
    return doc_data["percentageNegotiated"] / 100 if len(doc_data) else 0
