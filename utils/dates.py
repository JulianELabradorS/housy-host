from datetime import datetime


def get_month_str(date) -> str:
    stringDate = date.split(" ")[0]
    monthNumber = datetime.strptime(stringDate, "%Y-%m-%d").month

    if monthNumber == 1:
        return "Enero"
    if monthNumber == 2:
        return "Febrero"
    if monthNumber == 3:
        return "Marzo"
    if monthNumber == 4:
        return "Abril"
    if monthNumber == 5:
        return "Mayo"
    if monthNumber == 6:
        return "Junio"
    if monthNumber == 7:
        return "Julio"
    if monthNumber == 8:
        return "Agosto"
    if monthNumber == 9:
        return "Septiembre"
    if monthNumber == 10:
        return "Octubre"
    if monthNumber == 11:
        return "Noviembre"
    if monthNumber == 12:
        return "Diciembre"

    return "Error"


def get_month(date) -> str:
    stringDate = date.split(" ")[0]
    monthNumber = datetime.strptime(stringDate, "%Y-%m-%d").month
    return monthNumber


def get_year(date) -> str:
    stringDate = date.split(" ")[0]
    return datetime.strptime(stringDate, "%Y-%m-%d").year
