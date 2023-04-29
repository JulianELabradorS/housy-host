from firebase_admin import firestore

from repositories.base_repository import get_firestore_client
from models.reservation import get_reservation_object
from dateutil.relativedelta import relativedelta
from repositories.property_repository import get_property_commission_percentage

firestore_client = get_firestore_client()


def save_prorated_reservation(tabulated_reservation):
    for data in tabulated_reservation:
        document = firestore_client.collection(
        "prorated_reservations").document(str(data["id"]))
        document.set(data)
    return tabulated_reservation


def update_prorated_reservation(tabulated_reservation):
    query = firestore_client.collection("prorated_reservations").where(
        'reservationId', '==', tabulated_reservation[-1]["reservationId"])
    docs = query.get()
    for doc in docs:
        doc.reference.delete()
    return save_prorated_reservation(tabulated_reservation)


def get_prorated_reservations(limit, start_at, propertyId, date):
    query = firestore_client.collection("prorated_reservations")
    tabulated_reservations = []
    # Aplicar filtros iniciales
    query = query.order_by(
        'id', direction=firestore.Query.DESCENDING)
    if (date):
        query = query.where("monthNumber", "==", date.month).where(
            "year", "==", date.year)
    if (propertyId):
        query = query.where('listingMapId', '==', int(propertyId))
    if (start_at):
        query = query.start_at({u'id': start_at})
    query = query.limit(int(limit))
    result = query.get()
    for reservation in result:
        reservation_dict = reservation.to_dict()
        date_fields = ["arrivalDate", "departureDate"]
        for field in date_fields:
            if reservation_dict[field]:
                reservation_dict[field] = reservation_dict[field].isoformat()
        tabulated_reservations.append(reservation_dict)
    return {'data': tabulated_reservations,
            'last_id': tabulated_reservations[-1]["id"] if len(tabulated_reservations) else None}


def get_prorated_data_by_reservation_id(reservationId):
    result = firestore_client.collection("prorated_reservations").where(
        'reservationId', '==', int(reservationId)).get()
    return {"data": [doc.to_dict() for doc in result]}


def update_budgeted_trm_on_data(trm_start_date, trm_value):
    tabulated_data = firestore_client.collection("prorated_reservations").where(
        "monthNumber", "==", trm_start_date.month).where("year", "==", trm_start_date.year).stream()
    for entry in tabulated_data:
        entry_data = entry.to_dict()
        if entry_data["currency"] == 'USD':
            entry_data["budgetedTrm"] = trm_value
            update_dict = recalculation_prorated_reservation(entry_data)
            entry.reference.update(update_dict)


def update_real_trm_on_data(start_date, end_date, trm_value):
    start = start_date
    while start < end_date:
        tabulated_data = firestore_client.collection("prorated_reservations").where(
            "arrivalDate", "==", start).stream()
        for entry in tabulated_data:
            entry_data = entry.to_dict()
            entry_data["realTrm"] = trm_value
            updated_dict = recalculation_prorated_reservation(entry_data)
            entry.reference.update(updated_dict)
        start = start + relativedelta(days=1)


def update_real_totals_in_prorrated_reservations(reservation_id, currency, total_paid, total_paid_cleaning):
    tabulated_data = firestore_client.collection("prorated_reservations").where(
        "reservationId", "==", int(reservation_id)).order_by(
        'id', direction=firestore.Query.ASCENDING).stream()
    for index, entry in enumerate(tabulated_data):
        entry_data = entry.to_dict()
        price_per_night= total_paid / entry_data["totalNights"]
        prorrated_total_paid = price_per_night * entry_data["nights"]
        entry_data["realValueReceived"] = prorrated_total_paid
        entry_data["realCleaningFee"] = total_paid_cleaning if index == 0 else 0
        entry_data["realValuesCurrency"] = currency
        update_dict = recalculation_prorated_reservation(entry_data)
        entry.reference.update(update_dict)


def update_property_percentage_in_proprrated_reservations(listingId, percentage):
    tabulated_data = firestore_client.collection("prorated_reservations").where(
        "listingMapId", "==", int(listingId)).stream()
    for entry in tabulated_data:
        entry_data = entry.to_dict()
        entry_data["listingCommissionPercentage"] = percentage/100
        update_dict = recalculation_prorated_reservation(entry_data)
        entry.reference.update(update_dict)

            
def recalculation_prorated_reservation(prorrated_dict):
    currency = prorrated_dict["currency"]
    total = prorrated_dict["totalCalculated"]
    baseCleaningFee = prorrated_dict["baseCleaningFee"]
    commission = prorrated_dict["listingCommissionPercentage"]
    budgetedTrm = prorrated_dict["budgetedTrm"]
    realTrm = prorrated_dict["realTrm"]    
    budgetedTotal = total * budgetedTrm if currency == 'USD' else total
    budgetedCommission = budgetedTotal * commission
    
    realValueReceived = prorrated_dict["realValueReceived"]
    convertedRealValueReceived = realValueReceived * realTrm if prorrated_dict["realValuesCurrency"] == 'USD' and realTrm else realValueReceived

    realCleaningFee=prorrated_dict["realCleaningFee"]
    convertedRealCleaningFee =realCleaningFee * realTrm if prorrated_dict["realValuesCurrency"] == 'USD' and realTrm else realCleaningFee
    realCommission = convertedRealValueReceived * commission
    netProprietary = convertedRealValueReceived - realCommission
    
    calculations_dict =  {
            "listingCommissionPercentage":commission,
            "budgetedTrm":budgetedTrm,
            "realTrm":realTrm,
            "budgetedTotal": budgetedTotal,
            "budgetedCleaningFee": baseCleaningFee * budgetedTrm if currency == 'USD' else baseCleaningFee,
            "budgetedCommission": budgetedCommission,
            "realValueReceived":realValueReceived,
            "convertedRealValueReceived":convertedRealValueReceived,
            "realCleaningFee":realCleaningFee,
            "convertedRealCleaningFee":convertedRealCleaningFee,
            "realCommission": realCommission,
            "netProprietary": netProprietary,
            "realValuesCurrency":prorrated_dict["realValuesCurrency"]
        }
    return calculations_dict
