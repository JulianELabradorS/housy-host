from constants.columns import COLUMNS_TO_MODIFY_BY_TRM
from models.reservation import Reservation
from repositories.property_repository import get_property
from utils.dates import get_month, get_month_str, get_year


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
        reservation["totalPriceCOP"] if "totalPriceCOP" in reservation else "",
        reservation['aseoPptoCOP'] if 'aseoPptoCOP' in reservation else "",
        reservation['comisionPptoCOP'] if 'comisionPptoCOP' in reservation else "",
        reservation['comisionRealCOP'] if 'comisionRealCOP' in reservation else "",
        reservation['netoPropietarioCOP'] if 'netoPropietarioCOP' in reservation else "",
        reservation['presupuestoRealCOP'] if 'presupuestoRealCOP' in reservation else "",
        reservation['aseoRealCOP'] if 'aseoRealCOP' in reservation else "",
        reservation['trmReal'] if 'trmReal' in reservation else "",
        reservation['arrivalDate'] if 'arrivalDate' in reservation else "",
    )


def get_property_last_trm(listingName: str):
    property = get_property(listingName)

    if (len(property.trms) == 0):
        return 4700

    return property.trms[-1].trm


def get_property_last_negotiation(listingName: str):
    property = get_property(listingName)

    if (len(property.negotiations) == 0):
        return 0.2

    try:
        return property.negotiations[-1].percentage
    except:
        return 0.2


def transform_to_COP(reservation):
    if ("trmReal" in reservation):
        trmReal = reservation['trm'] if reservation["trmReal"] == "" else reservation['trmReal']

    trm = reservation["trm"]

    if (reservation["currency"] == 'COP'):
        reservation['totalPriceCOP'] = reservation["totalPrice"]
        for column in COLUMNS_TO_MODIFY_BY_TRM:
            if (column not in reservation):
                reservation[column+"COP"] = 0
            else:
                reservation[column+"COP"] = reservation[column]

        return reservation

    reservation['totalPriceCOP'] = float(reservation["totalPrice"]
                                         ) * float(trm)

    for column in COLUMNS_TO_MODIFY_BY_TRM:
        if (column not in reservation):
            reservation[column+"COP"] = 0
            continue

        if (reservation[column] != None and reservation[column] != ""):
            if (("Real" in column or "real" in column) and "trmReal" in reservation):
                reservation[column +
                            "COP"] = float(reservation[column]) * float(trmReal)
            else:
                reservation[column +
                            "COP"] = float(reservation[column]) * float(trm)

    return reservation


def complete_columns_data(reservation):
    if "aseoPpto" not in reservation:
        reservation["aseoPpto"] = reservation["airbnbListingCleaningFee"] if reservation[
            "channelName"] == "airbnbOfficial" else reservation["cleaningFee"]
    if "aseoReal" not in reservation:
        reservation["aseoReal"] = reservation["aseoPpto"]
    reservation["mes"] = get_month_str(reservation["reservationDate"])
    reservation["monthNumber"] = get_month(reservation["reservationDate"])
    reservation["anio"] = get_year(reservation["reservationDate"])

    return reservation


def calculate_columns_new_reservation(reservation):
    reservation['negociacion'] = get_property_last_negotiation(
        reservation["listingName"])
    reservation['trm'] = get_property_last_trm(reservation["listingName"])

    reservation = complete_calculated_columns_of_negotiation(reservation)
    reservation = transform_to_COP(reservation)

    return reservation


def complete_calculated_columns_of_negotiation(reservation):
    negotiationPercentage = float(
        reservation["negociacion"]) if "negociacion" in reservation else 0.2

    reservation["comisionPpto"] = negotiationPercentage * \
        float(reservation["totalPrice"])

    if (("presupuestoReal" in reservation) and ("aseoReal" in reservation) and (reservation["presupuestoReal"] != "") and (reservation["aseoReal"] != "")):
        reservation["comisionReal"] = negotiationPercentage * \
            (float(reservation["presupuestoReal"]) -
             float(reservation["aseoReal"]))

        reservation["netoPropietario"] = float(reservation["presupuestoReal"]) - \
            float(reservation["comisionReal"])

    # reservation["comisionPptoCOP"] = negotiationPercentage * \
    #     int(reservation["totalPriceCOP"])

    # if ("presupuestoReal" in reservation):
    #     reservation["comisionRealCOP"] = negotiationPercentage * \
    #         (int(reservation["presupuestoRealCOP"]) -
    #          int(reservation["aseoRealCOP"]))

    #     reservation["netoPropietarioCOP"] = int(reservation["presupuestoRealCOP"]) - \
    #         int(reservation["comisionRealCOP"])

    return reservation
