from flask import Flask, request
from flask_ngrok import run_with_ngrok
import reservations_service

RESERVATION_UPDATED = "reservation.updated"
RESERVATION_CREATED = "reservation.created"

app = Flask(__name__)
run_with_ngrok(app)


@app.route("/load-reservations")
def load_reservations():
    reservations_service.load_reservations()
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


if __name__ == "__main__":
    app.run()
