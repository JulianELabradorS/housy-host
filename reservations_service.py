import requests
import time
import reservations_repository

limit = 500
offset = 0
url = "https://api.hostaway.com/v1/reservations?limit=" + \
    str(limit) + "&offset="
headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0MzA4NSIsImp0aSI6ImEzMWI0NzY4MjBjNzUyYTg4ZjQxYjM3MGQwMzJkNDFhNmUzMDUyMTJhZWE5NjI0ZDFmNGE2N2Q2YWViM2QwOTRmYmViZjIxMmU3MzNlNmYwIiwiaWF0IjoxNjcwMTY3NzU4LCJuYmYiOjE2NzAxNjc3NTgsImV4cCI6MTczMzMyNjE1OCwic3ViIjoiIiwic2NvcGVzIjpbImdlbmVyYWwiXSwic2VjcmV0SWQiOjk5Nzd9.mvQzq_BYV6wMH8qP09LgpBXcKmAbMZioRvInHJsgq-IZY7JFnzMHyCHQ-6O63f_CirtI2uOENwd-7e7EM0gXCvp9Vwx9VFDwj89fUztsWAEFzH_JvD_fwIWgkBBdOfDxIVTriV3u_QbTEzrilC-7md1pHPJV1b0QroljPkdgh1Q', 'Accept': 'application/json'}


def getReservations():
    global offset
    response = requests.get(
        url + str(offset), headers=headers).json()

    offset = offset + len(response['result'])

    print("Number of reservations loaded: " + str(offset) +
          "\nAnd this result: " + str(len(response['result'])))

    result = reservations_repository.save_reservations(response['result'])
    print(result)

    return response


def load_reservations():
    start_time = time.time()

    response = getReservations()

    while (len(response['result']) == limit):
        try:
            response = getReservations()
        except Exception as e:
            print(e)
            return ("ERROR: Exception: %" % e)

    print("\nIt took %s seconds" % (time.time() - start_time))

    return "All reservations were loaded succesfully"


def create_reservation(reservation):
    result = reservations_repository.create_reservation(reservation)
    print(result)


def update_reservation(reservation):
    result = reservations_repository.update_reservation(reservation)
    print(result)
