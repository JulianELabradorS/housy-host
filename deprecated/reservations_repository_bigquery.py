from dotenv import load_dotenv
from google.cloud import bigquery
import pandas

load_dotenv()
TABLE_ID = bigquery.Table.from_string("tribal-joy-378015.hostaway.Reserva")


client = bigquery.Client()
print(client)


def get_row(id):
    query = "SELECT id FROM hostaway.Reserva WHERE id = '{}'".format(str(id))
    query_job = client.query(query)
    rows = query_job.result()
    return rows.total_rows


def insert_rows_from_list(reservations):
    reservations = clean_reservation_list(reservations)

    errors = client.insert_rows_json(TABLE_ID, reservations)
    if errors == []:
        print("New rows inserted")
    else:
        print("Encontered errors while inserting rows: {}".format(errors))


def update_row(reservation):
    if (get_row(reservation['id']) == 0):
        insert_rows_from_list([reservation])

    reservation = clean_reservation_list([reservation])[0]
    reservation_keys = reservation.keys()

    sql_statement = "UPDATE hostaway.Reserva SET"
    for key in reservation_keys:
        if (key != "id"):
            value = "'{}'".format(str(reservation[key])
                                  ) if reservation[key] != None else 'null'
            sql_statement += " " + str(key) + " = " + \
                value + " ,"
    sql_statement = sql_statement[:-1]
    sql_statement += " WHERE id = '{}'".format(str(reservation['id']).strip())

    query_job = client.query(sql_statement)
    rows = query_job.result()

    print("updated: {}".format(rows))


def clean_reservation_list(reservations):
    cleanReservations = []
    for reservation in reservations:
        del reservation['reservationUnit']
        del reservation['reservationFees']
        del reservation['financeField']
        del reservation['customFieldValues']
        del reservation['listingCustomFields']
        del reservation['guestNote']
        del reservation['hostNote']
        cleanReservations.append(reservation)

    return cleanReservations
