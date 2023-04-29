from flask import abort
from firebase_admin import firestore
from repositories.base_repository import get_firestore_client
from models.budgeted_trm import BudgetedTrm
import repositories.prorated_reservation_repository as prorated_reservation_repository
firestore_client = get_firestore_client()


def create_budgeted_trm(initial_date, value):
    doc_ref = firestore_client.collection("budgeted_trms").where(
        'startDate', '==', initial_date).get()
    if len(doc_ref) > 0:
        return 'There is already a trm assigned to this month', 400
    created_trm = BudgetedTrm(
        value, initial_date, initial_date.month, initial_date.year)
    firestore_client.collection("budgeted_trms").add(created_trm.to_dict())
    prorated_reservation_repository.update_budgeted_trm_on_data(initial_date, value)
    return {"success": True}


def get_budgeted_trm_of_month(month_number, year):
    query = firestore_client.collection("budgeted_trms").where(
        'monthNumber', '==', month_number).where(
        'year', '==',  year)
    doc_data = [doc.to_dict() for doc in query.stream()]
    return  doc_data[0]["value"] if len(doc_data) else 0


def get_all_budgeted_trm_by_year(year):
    query = firestore_client.collection("budgeted_trms").order_by(
        'startDate', direction=firestore.Query.DESCENDING)
    if year:
        query = query.where(
            'year', '==', int(year))
    data = []
    for doc in query.get():
        doc_dic = doc.to_dict()
        doc_dic["id"] = doc.id
        doc_dic["startDate"] = doc_dic["startDate"].strftime("%B, %Y")
        data.append(doc_dic)
    return {"data": data}


def update_budgeted_trm(id, value):
    doc_ref = firestore_client.collection(
        "budgeted_trms").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        return 'there is no trm with this id', 404
    budgeted_trm = doc.to_dict()
    doc_ref.update({"value": value})
    budgeted_trm["value"] = value
    prorated_reservation_repository.update_budgeted_trm_on_data(
         budgeted_trm["startDate"],  budgeted_trm["value"])
    return {"success": True}
