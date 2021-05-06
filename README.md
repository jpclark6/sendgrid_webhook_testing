# SendGrid webhook auth testing

Testing authentication with non-ascii characters in parts of SendGrid webhook message.


## Methodology

Send an email through SendGrid that will eventually cause a webhook event that includes a non-ascii character in the payload. Set up basic Flask app on Heroku to run through the basic authentication script and print the outputs. See app.py for details.

In this case it is by adding a link with the character "é" so that when the link is clicked it sends a click webhook event with that character in the "url" value of the payload.

See the file send_message.py for the exact code and message.

Set up a basic web app to authenticate the payload and print out the response. Cause an "open" event that doesn't include the special character and and view the result. Cause a click event that includes the "é" character.

## Results

The message that did not include the special character was correctly authenticated. The message that did include the special character was not authenticated.

Correctly authenticated message from logs

```
Payload: '[{"email":"padiko1105@drluotan.com","event":"open","ip":"xxx.xxx.xxx.xxx","sg_content_type":"html","sg_event_id":"lvPaxhihT6qB8ZHu26WRHQ","sg_message_id":"CDd0Q90kTcyShLwdFkMdxg.filterdrecv-79b6969b64-mdqmv-1-6094524B-167.0","timestamp":1620334630,"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'
Timestamp: '1620334643'
Signature: 'MEYCIQDwobQhZKhbftob3nHjljj63olFjm2zpb28MMpgCu5ufwIhAPuJwS4hqSjzuNAYpuHZoPCOF0LBLnQTdwysOHnEmsQU'
Authenticated: True
```

Falsely rejected message from logs

```
Payload: '[{"email":"padiko1105@drluotan.com","event":"click","ip":"xxx.xxx.xxx.xxx","sg_event_id":"CrGNumiJQZWsjFRBmf2XXQ","sg_message_id":"CDd0Q90kTcyShLwdFkMdxg.filterdrecv-79b6969b64-mdqmv-1-6094524B-167.0","timestamp":1620334754,"url":"https://example.com?test=Daré","url_offset":{"index":0,"type":"html"},"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'
Timestamp: '1620334768'
Signature: 'MEUCIQDFv0s0m0kEevGdKJ69/NpEmKwnzltX4YMGst7Xmjau/AIgdC/cfUGZ/+gaJ9MuZ7cfkTMDKDmcgxUG1vG2AFepxmU='
Authenticated: False
```

## Required env vars

### App only (Heroku)

* PUBLIC_SENDGRID_KEY=key to authenticate messages

### To send email (send_message.py)

* FROM_EMAIL=email you're authorized to send from
* TO_EMAIL=email address you're able to open message and click link
* SENDGRID_API_KEY=self explanitory

### To deploy to Heroku

```bash
$ heroku create
$ git push heroku master
```
