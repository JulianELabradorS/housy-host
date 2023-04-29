from flask import abort
from repositories.base_repository import get_firestore_client
from datetime import datetime
from models.real_trm import RealTrm
from firebase_admin import firestore
from dateutil.relativedelta import relativedelta
import repositories.prorated_reservation_repository as prorated_reservation_repository
firestore_client = get_firestore_client()



def create_real_trm(start_date, end_date, value):
    exists_trm = check_if_there_is_an_assigned_trm(start_date)
    if exists_trm:
        return 'there is a term assigned to this date range', 400
    created_trm = RealTrm(
        value, start_date, end_date, datetime.now().year)
    firestore_client.collection("real_trms").add(created_trm.to_dict())
    prorated_reservation_repository.update_real_trm_on_data(
        start_date, end_date, value)
    return {"success": True}


def get_real_trm_of_date(check_in_date):
    query = firestore_client.collection("real_trms").where(
        'startDate', '<=', check_in_date).order_by(
        'startDate', direction=firestore.Query.DESCENDING).limit(1)
    doc_data = [doc.to_dict() for doc in query.stream()]
    return doc_data[0]["value"] if len(doc_data) else 0


def get_all_real_trm_added_by_year(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    query = firestore_client.collection("real_trms").where(
        'startDate', '>=', start_date).where('startDate', '<=', end_date).get()
    trms = []
    for doc in query:
        doc_dic = doc.to_dict()
        doc_dic["id"] = doc.id
        doc_dic["startDate"] = doc_dic["startDate"].strftime("%Y-%m-%d")
        doc_dic["endDate"] = doc_dic["endDate"].strftime("%Y-%m-%d")
        trms.append(doc_dic)
    return {"data": trms}


def update_real_trm(id, value, start_date, end_date):
    exists_trm = check_if_there_is_an_assigned_trm(start_date)
    if exists_trm:
        return 'there is a term assigned to this date range', 400
    doc_ref = firestore_client.collection(
        "real_trms").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        return 'there is no trm with this id', 404
    real_trm = doc.to_dict()
    doc_ref.update(
        {"value": value, "startDate": start_date, "endDate": end_date})
    real_trm["value"] = value
    prorated_reservation_repository.update_real_trm_on_data(
        start_date, end_date, value)
    return {"success": True}

def check_if_there_is_an_assigned_trm(start_date):
    query = firestore_client.collection("real_trms").where(
        'startDate', '<=', start_date).order_by(
        'startDate', direction=firestore.Query.DESCENDING).limit(1)
    doc_data = [doc.to_dict() for doc in query.stream()]
    return doc_data[0]['endDate'] >= start_date if len(doc_data) else False
    
