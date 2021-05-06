import os

from flask import Flask, request, jsonify
from sendgrid.helpers.eventwebhook import EventWebhook


app = Flask(__name__)


def authenticate(signature, timestamp, payload):
    PUBLIC_SENDGRID_KEY = os.getenv("PUBLIC_SENDGRID_KEY")
    webhook = EventWebhook(PUBLIC_SENDGRID_KEY)
    authenticated = webhook.verify_signature(payload, signature, timestamp)
    return authenticated


@app.route('/webhook', methods=['POST'])
def post_something():
    print("Testing webhook")
    try:
        payload = request.data.decode('utf-8')
        timestamp = request.headers['x-twilio-email-event-webhook-timestamp']
        signature = request.headers['x-twilio-email-event-webhook-signature']

        authenticated = authenticate(signature, timestamp, payload)

        print(f"Payload: '{payload}'")
        print(f"Timestamp: '{timestamp}'")
        print(f"Signature: '{signature}'")
        print(f"Authenticated: {authenticated}")

        return jsonify({"status": 200})
    except Exception as e:
        print("Ran into an error", e)
        return jsonify({
            "error": str(e)
        })

@app.route('/')
def index():
    return "<h1>Hello world!</h1>"
