from json import dumps

from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.signature import Signature
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.utils.file import File
from sendgrid.helpers.eventwebhook import EventWebhook
import requests


publicKeyPem = File.read("publicKey.pem")
publicKey = PublicKey.fromPem(publicKeyPem)

privateKeyPem = File.read("privateKey.pem")
privateKey = PrivateKey.fromPem(privateKeyPem)

def send_mock_webhook(payload, timestamp):
    message = timestamp + payload
    signature = Ecdsa.sign(message, privateKey)
    base64_signature = signature.toBase64()
    # print("Verified:", Ecdsa.verify(message, signature, publicKey))
    url = 'https://cryptic-caverns-35958.herokuapp.com/mock_webhook'
    headers = {'x-twilio-email-event-webhook-timestamp': timestamp, 'x-twilio-email-event-webhook-signature': base64_signature}
    data = payload.encode('utf-8')

    response = requests.post(url, headers=headers, data=data)

    return response.json()

good_payload = '{"email":"rarabor719@threepp.com","event":"open","ip":"xxx.xxx.xxx.xxx","sg_content_type":"html","sg_event_id":"j0NhGx01TCimNpTmBEN0Yg","sg_message_id":"m7BqO7JsQ_Obv9nkaA-sCA.filterdrecv-77df4fc8dd-6h694-1-609974BE-A5.0","timestamp":1620669695,"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'
timestamp = '1620669695'
response = send_mock_webhook(good_payload, timestamp)
print("Working payload", response)

bad_payload = '[{"email":"rarabor719@threepp.com","event":"click","ip":"xxx.xxx.xxx.xxx","sg_event_id":"EEKhxyYSSjCQ4M92ZUTVtg","sg_message_id":"m7BqO7JsQ_Obv9nkaA-sCA.filterdrecv-77df4fc8dd-6h694-1-609974BE-A5.0","timestamp":1620669695,"url":"https://example.com?test=Daré","url_offset":{"index":0,"type":"html"},"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'
timestamp = '1620669695'
response = send_mock_webhook(bad_payload, timestamp)
print("Broken payload", response)
