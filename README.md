# SendGrid webhook auth testing

Testing authentication with non-ascii characters in parts of SendGrid webhook message.


## Methodology

### Testing SendGrid Webhook

Send an email through SendGrid that will eventually cause a webhook event that includes a non-ascii character in the payload. Set up basic Flask app on Heroku to run through the basic authentication script and print the outputs. See app.py for details.

In this case it is by adding a link with the character "é" so that when the link is clicked it sends a click webhook event with that character in the "url" value of the payload.

See the file send_message.py for the exact code and message.

Set up a basic web app to authenticate the payload and print out the response. Cause an "open" event that doesn't include the special character and and view the result. Cause a click event that includes the "é" character.

### Testing Signing and Verifying

Using the starkbank/ecdsa-python package that the SendGrid python package uses to verify the messages create a private and public key, then upload the public key to the server. Create payloads that match the passing and failing payloads from above. Create signatures, then send to the server using the updated public key.

Check the status of whether the webhooks are passing or failing.

## Results

### SendGrid  Webhook

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

### Signing and Verifying

When we signed the webhooks ourselves we were able to get both to pass, leading us to believe that our authentication on the server works correctly, and that the package can handle characters correctly. It leads us to believe something may be wrong with the signature we are receiving from SendGrid.

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

### To use mock webhook

Create keys

```bash
$ openssl ecparam -name secp256k1 -genkey -out privateKey.pem
$ openssl ec -in privateKey.pem -pubout -out publicKey.pem
```

Update the URL for heroku and run mock_webhook.py