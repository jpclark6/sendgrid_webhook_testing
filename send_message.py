# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

html_message = '<p>Hello <a href="https://example.com?test=Daré">test</a></p>'

message = Mail(
    from_email='test@jclarkdev.com',
    to_emails='padiko1105@drluotan.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content=html_message)
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)