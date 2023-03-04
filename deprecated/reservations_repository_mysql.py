from google.cloud.sql.connector import Connector
import sqlalchemy
from dotenv import load_dotenv
from models.reservation import Reservation

load_dotenv()

INSTANCE_CONNECTION_NAME = f"tribal-joy-378015:us-central1:mysql-db"
DB_USER = "root"
DB_PASS = "password123"
DB_NAME = "hostaway"

# initialize Connector object
connector = Connector()

# function to return the database connection object


def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn


# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)


def get_reservations():
    with pool.connect() as db_conn:
        results = db_conn.execute(sqlalchemy.text(
            "SELECT * FROM hostaway.reserva")).fetchall()

        reservations_list = []
        for result in results:
            reservations_list.append(Reservation(
                result[87],
                result[101],
                result[47],
                result[65],
                result[30] if result[25] != "airbnb" else result[7],
                result[90],
                result[25],
                result[109],
                result[53]
            ))
        return (reservations_list)


def get_row(id):
    with pool.connect() as db_conn:
        query = "SELECT id FROM reserva WHERE id = '{}'".format(str(id))
        results = db_conn.execute(sqlalchemy.text(
            query)).fetchall()

        return len(results)


def build_insert_query(reservations):
    reservations = clean_reservation_list(reservations)
    query = "INSERT INTO hostaway.reserva ("

    for key in reservations[0].keys():
        query += "{},".format(str(key))
    query = query[:-1]
    query += ") VALUES ("

    for reservation in reservations:
        for key in reservation:
            query += "'{}'".format(str(reservation[key]).replace("'", "")
                                   ) if reservation[key] != None else 'null'
            query += ","
        query = query[:-1]
        query += "), ("

    query = query[:-3]
    query += ";"

    return query


def insert_rows_from_list(reservations):
    with pool.connect() as db_conn:
        reservations = clean_reservation_list(reservations)

        query = build_insert_query(reservations)

        result = db_conn.execute(sqlalchemy.text(query))
        db_conn.commit()

        return result

    # if errors == []:
    #     print("New rows inserted")
    # else:
    #     print("Encontered errors while inserting rows: {}".format(errors))


def update_row(reservation):
    if (get_row(reservation['id']) == 0):
        return insert_rows_from_list([reservation])

    reservation = clean_reservation_list([reservation])[0]
    reservation_keys = reservation.keys()

    sql_statement = "UPDATE hostaway.reserva SET"
    for key in reservation_keys:
        if (key != "id"):
            value = "'{}'".format(str(reservation[key]).replace("'", "")
                                  ) if reservation[key] != None else 'null'
            sql_statement += " " + str(key) + " = " + \
                value + " ,"
    sql_statement = sql_statement[:-1]
    sql_statement += " WHERE id = '{}'".format(str(reservation['id']).strip())
    sql_statement += ";"

    with pool.connect() as db_conn:
        result = db_conn.execute(sqlalchemy.text(sql_statement))
        db_conn.commit()


def clean_reservation_list(reservations):
    cleanReservations = []
    for reservation in reservations:
        for key in ['reservationUnit',
                    'reservationFees',
                    'financeField',
                    'customFieldValues',
                    'listingCustomFields',
                    'guestNote',
                    'hostNote',
                    'comment',
                    'guestPicture',
                    'guestWork',
                    'guestEmail',
                    'guestAddress',
                    'guestFirstName',
                    'guestLastName',
                    'guestName',
                    'guestPortalRevampUrl',
                    'guestPortalUrl',
                    'guestRecommendations']:
            if key in reservation:
                del reservation[key]

        cleanReservations.append(reservation)

    return cleanReservations


def calculated_columns(reservation):
    # reservation["comisionPpto"] = reservation["totalPrice"] * Negociacion
    # reservation["comisionReal"] = reservation[""]
    pass
