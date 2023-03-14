import json
import asyncio
from flask import Flask, request
from flask_cors import CORS, cross_origin
# from flask_ngrok import run_with_ngrok
import reservations_service

RESERVATION_UPDATED = "reservation.updated"
RESERVATION_CREATED = "reservation.created"

app = Flask(__name__)
cors = CORS(app)
# run_with_ngrok(app)


@app.route("/")
@cross_origin()
def test():
    return "API Working", 200


@app.route("/load-reservations")
def load_reservations():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(reservations_service.load_reservations())
    loop.run_forever()

    return "The load proceess started", 200


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


@app.route("/reservations", methods=["GET"])
@cross_origin()
def get_reservations():
    result = reservations_service.get_reservations()
    return json.dumps([obj.__dict__ for obj in result]), 200


@app.route("/paginated-reservations", methods=["GET"])
@cross_origin()
def get_paginated_reservations():
    limit = request.args.get("limit")
    start_at = request.args.get("start_at")

    order_by = request.args.get("order_by")
    order_by = order_by if order_by != None else "id"

    direction = request.args.get("direction")
    direction = direction if direction != None else "descending"

    result = reservations_service.get_paginated_reservations(
        limit, start_at, order_by, direction)

    return json.dumps(result), 200


if __name__ == "__main__":
    app.run()
