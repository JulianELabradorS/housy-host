import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
import services.initial_config_service as initial_config_service
import services.reservations_service as reservations_service
import services.properties_service as properties_service
import services.budgeted_trm_service as budgeted_trm_service
import services.real_trm_service as real_trm_service
import services.prorated_reservations_service as prorated_reservations_service
from datetime import datetime

RESERVATION_UPDATED = "reservation.updated"
RESERVATION_CREATED = "reservation.created"

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
@cross_origin()
def test():
    return "API Working", 200

# Enpoint for uploading initial information to the database


@app.route("/initial-config")
def load_initial_config():
    initial_config_service.load_properties()
    initial_config_service.load_reservations()
    return "The load proceess started", 200

# Webhokk to capture changes in hostaway


@app.route("/unified-webhook", methods=['POST'])
def unified_webhook():
    parsedRequest = request.json

    if "event" in parsedRequest:
        if (parsedRequest['event'] == RESERVATION_CREATED):
            reservations_service.create_reservation(parsedRequest["data"])

        elif (parsedRequest['event'] == RESERVATION_UPDATED):
            reservations_service.update_reservation(parsedRequest["data"])

        print("\nData received from Webhook is: ", parsedRequest)
    print("\n")

    return "Success", 200

# RESERVATIONS


@app.route("/paginated-reservations", methods=["GET"])
@cross_origin()
def get_paginated_reservations():
    limit = request.args.get("limit")
    start_at = request.args.get("start_at")
    propertyId = request.args.get("propertyId")
    date = datetime.fromisoformat(request.args.get("date").replace(
        'Z', '+00:00')) if request.args.get("date") else None
    result = reservations_service.get_paginated_reservations(
        limit, start_at, propertyId, date)

    return json.dumps(result), 200

@app.route("/reservations/<id>", methods=["PATCH"])
@cross_origin()
def update_reservation(id):
    data = request.get_json()
    result = reservations_service.update_fields_in_reservation(id, data)
    return result

# PRORATED RESERVATIONS


@app.route("/prorated-reservations", methods=['GET'])
@cross_origin()
def get_reservation_prorated_data():
    limit = request.args.get("limit")
    start_at = request.args.get("start_at")
    propertyId = request.args.get("propertyId")
    date = datetime.fromisoformat(request.args.get("date").replace(
        'Z', '+00:00')) if request.args.get("date") else None
    result = prorated_reservations_service.get_prorated_reservations(
        limit, start_at, propertyId, date)

    return result

# PROPERTIES


@app.route("/properties", methods=["GET"])
@cross_origin()
def get_properties():
    result = properties_service.get_all_properties()
    return json.dumps(result)


@app.route("/properties/<id>", methods=['PATCH'])
@cross_origin()
def get_one_property(id):
    data = request.get_json()
    result = properties_service.update_percentage_negotiated(id,data)
    return result

# Budgueted TRM


@app.route("/budgeted-trm", methods=['GET'])
@cross_origin()
def get_all_budgeted_trms_by_year():
    year = request.args.get("year")
    result = budgeted_trm_service.get_all_budgeted_trm_of_year(year)
    return result


@app.route("/budgeted-trm", methods=['POST'])
@cross_origin()
def create_budgeted_trm():
    data = request.get_json()
    result = budgeted_trm_service.create_budgeted_trm(data)
    return result


@app.route("/budgeted-trm/<id>", methods=['POST'])
@cross_origin()
def update_budgeted_trm(id):
    data = request.get_json()
    result = budgeted_trm_service.update_budgeted_trm(id, data)
    return result

# Budgueted TRM


@app.route("/real-trm", methods=['GET'])
@cross_origin()
def get_all_real_trms_by_year():
    year = request.args.get("year")
    result = real_trm_service.get_real_trm_by_year(year)
    return result


@app.route("/real-trm", methods=['POST'])
@cross_origin()
def create_real_trm():
    data = request.get_json()
    result = real_trm_service.create_real_trm(data)
    return result

@app.route("/real-trm/<id>", methods=['POST'])
@cross_origin()
def update_real_trm(id):
    data = request.get_json()
    result = real_trm_service.update_real_trm(id, data)
    return result


if __name__ == "__main__":
    app.run()
