import os

from flask import Flask, request, jsonify
from sendgrid.helpers.eventwebhook import EventWebhook


app = Flask(__name__)


def authenticate(signature, timestamp, payload, public_key=None):
    PUBLIC_SENDGRID_KEY = public_key or os.getenv("PUBLIC_SENDGRID_KEY")
    webhook = EventWebhook(PUBLIC_SENDGRID_KEY)
    authenticated = webhook.verify_signature(payload, signature, timestamp)
    return authenticated


@app.route('/webhook', methods=['POST'])
def webhook():
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


@app.route('/mock_webhook', methods=['POST'])
def mock_webhook():
    print("Testing mock webhook")
    try:
        payload = request.data.decode('utf-8')
        timestamp = request.headers['x-twilio-email-event-webhook-timestamp']
        signature = request.headers['x-twilio-email-event-webhook-signature']

        public_key = os.getenv("PERSONAL_PUBLIC_SENDGRID_KEY")

        authenticated = authenticate(signature, timestamp, payload, public_key=public_key)

        print(f"Payload: '{payload}'")
        print(f"Timestamp: '{timestamp}'")
        print(f"Signature: '{signature}'")
        print(f"Authenticated: {authenticated}")

        return jsonify({"verified": authenticated})
    except Exception as e:
        print("Ran into an error", e)
        return jsonify({
            "error": str(e)
        })

@app.route('/')
def index():
    return "<h1>Hello world!</h1>"
