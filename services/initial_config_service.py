
import requests
import time
import repositories.reservations_repository as reservations_repository
import repositories.property_repository as property_repository


url = "https://api.hostaway.com/v1"
headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0MzA4NSIsImp0aSI6ImEzMWI0NzY4MjBjNzUyYTg4ZjQxYjM3MGQwMzJkNDFhNmUzMDUyMTJhZWE5NjI0ZDFmNGE2N2Q2YWViM2QwOTRmYmViZjIxMmU3MzNlNmYwIiwiaWF0IjoxNjcwMTY3NzU4LCJuYmYiOjE2NzAxNjc3NTgsImV4cCI6MTczMzMyNjE1OCwic3ViIjoiIiwic2NvcGVzIjpbImdlbmVyYWwiXSwic2VjcmV0SWQiOjk5Nzd9.mvQzq_BYV6wMH8qP09LgpBXcKmAbMZioRvInHJsgq-IZY7JFnzMHyCHQ-6O63f_CirtI2uOENwd-7e7EM0gXCvp9Vwx9VFDwj89fUztsWAEFzH_JvD_fwIWgkBBdOfDxIVTriV3u_QbTEzrilC-7md1pHPJV1b0QroljPkdgh1Q', 'Accept': 'application/json'}


def load_reservations():
    start_time = time.time()
    limit = 250
    offset = 0
    totalData = 4000
    while offset < totalData:
        try:
            response = requests.get(
                f'{url}/reservations?&sortOrder=arrivalDateDesc&limit={limit}&offset={offset}', headers=headers).json()
            reservations = response['result']
            reservations_repository.save_reservations(reservations)
            offset += offset + response['limit']
            """ totalData = response['count'] """
        except Exception as e:
            return ("ERROR: Exception: %" % e)

    print("\nIt took %s seconds to load reservations" %
          (time.time() - start_time))

    return "All reservations were loaded succesfully"


def load_properties():
    start_time = time.time()
    limit = 250
    offset = 0
    totalData = 250
    while (offset <= totalData):
        try:
            response = requests.get(
                f'{url}/listings?limit={limit}&offset={offset}', headers=headers).json()
            properties = response['result']
            property_repository.save_properties(properties)
            offset += offset + response['limit']
            totalData = response['count']
        except Exception as e:
            print(e)
            return ("ERROR: Exception: %" % e)

    print("\nIt took %s seconds to load properties" %
          (time.time() - start_time))

    return "All properties were loaded succesfully"
