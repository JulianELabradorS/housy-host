import requests
import time
from models.property import Property
import repositories.reservations_repository as reservations_repository
import repositories.property_repository as property_repository
from utils.columns_calculation import calculate_columns_new_reservation, complete_columns_data

limit = 250
offset = 0
url = "https://api.hostaway.com/v1/reservations?limit=" + \
    str(limit) + "&offset="
headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0MzA4NSIsImp0aSI6ImEzMWI0NzY4MjBjNzUyYTg4ZjQxYjM3MGQwMzJkNDFhNmUzMDUyMTJhZWE5NjI0ZDFmNGE2N2Q2YWViM2QwOTRmYmViZjIxMmU3MzNlNmYwIiwiaWF0IjoxNjcwMTY3NzU4LCJuYmYiOjE2NzAxNjc3NTgsImV4cCI6MTczMzMyNjE1OCwic3ViIjoiIiwic2NvcGVzIjpbImdlbmVyYWwiXSwic2VjcmV0SWQiOjk5Nzd9.mvQzq_BYV6wMH8qP09LgpBXcKmAbMZioRvInHJsgq-IZY7JFnzMHyCHQ-6O63f_CirtI2uOENwd-7e7EM0gXCvp9Vwx9VFDwj89fUztsWAEFzH_JvD_fwIWgkBBdOfDxIVTriV3u_QbTEzrilC-7md1pHPJV1b0QroljPkdgh1Q', 'Accept': 'application/json'}


def getHostawayReservations():
    global offset
    response = requests.get(
        url + str(offset), headers=headers).json()

    offset = offset + len(response['result'])

    print("Number of reservations loaded: " + str(offset) +
          "\nAnd this result: " + str(len(response['result'])))

    reservations = response['result']

    reservation = [complete_columns_data(
        reservation) for reservation in reservations]
    reservation = [calculate_columns_new_reservation(
        reservation) for reservation in reservations]

    reservations_repository.save_reservations(reservation)

    return response


def load_reservations():
    start_time = time.time()
    print("Started loading from Hostaway")

    response = getHostawayReservations()

    while (len(response['result']) == limit):
        try:
            response = getHostawayReservations()
        except Exception as e:
            print(e)
            return ("ERROR: Exception: %" % e)

    print("\nIt took %s seconds" % (time.time() - start_time))

    return "All reservations were loaded succesfully"


def create_reservation(reservation):
    result = reservations_repository.create_reservation(reservation)


def update_reservation(reservation):
    result = reservations_repository.update_reservation(reservation)


def get_reservations():
    return reservations_repository.get_reservations()


def get_paginated_reservations(limit, start_at, order_by, direction):
    return reservations_repository.get_paginated_reservations(limit, start_at, order_by, direction)


def get_properties():
    return property_repository.get_properties()


def update_property(property):
    result = property_repository.update_property(property)
    reservations_repository.update_computed_values(Property(property))

    return result
