import os
from sendgrid.helpers.eventwebhook import EventWebhook
from sendgrid.helpers.eventwebhook.eventwebhook_header import EventWebhookHeader


def authenticate(signature, timestamp, payload):
    PUBLIC_SENDGRID_KEY = os.getenv("PUBLIC_SENDGRID_KEY")
    webhook = EventWebhook(PUBLIC_SENDGRID_KEY)
    authenticated = webhook.verify_signature(payload, signature, timestamp)
    print("Authenticated:", authenticated)


signature = 'MEYCIQDWE406+i0ri2ThRYgrX+5Xuw2fMNHCYjQe0o2MV53U1gIhAIqxL+GhTo6QwaViV+7Xhi7IUYj8CSp6Xlrls1FJ7Tjp'
timestamp = '1620329607'
payload = '[{"email":"padiko1105@drluotan.com","event":"open","ip":"174.51.74.182","sg_content_type":"html","sg_event_id":"xbnsBNwARIWoKgyMZuw8MQ","sg_message_id":"mW1A57aIQSyd2wV2Sr89Ww.filterdrecv-79b6969b64-mdqmv-1-60944345-12.0","timestamp":1620329588,"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'

print("Normal message")
authenticate(signature, timestamp, payload)

signature = 'MEUCIQDFi8At5xnaHuuVEJynE5i2pvOetDhypaXgq2XR7EAOzwIgRQQL8LGEsjx3mKJd/Iu95fM2tND2flOF5vbgK19ADOQ='
timestamp = '1620329319'
payload = '[{"email":"padiko1105@drluotan.com","event":"click","ip":"174.51.74.182","sg_event_id":"YUIr9y2wQ7e8wApQXzdmjg","sg_message_id":"mW1A57aIQSyd2wV2Sr89Ww.filterdrecv-79b6969b64-mdqmv-1-60944345-12.0","timestamp":1620329309,"url":"https://example.com?test=Daré","url_offset":{"index":0,"type":"html"},"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'

print("\nWeird message")
authenticate(signature, timestamp, payload)