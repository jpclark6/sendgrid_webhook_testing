# SendGrid webhook auth testing

Testing authentication with non-ascii characters in parts of SendGrid webhook message.


## Methodology

### Testing SendGrid Webhook

Send an email through SendGrid that will eventually cause a webhook event that includes a non-ascii character in the payload. Set up basic Flask app on Heroku to run through the basic authentication script and print the outputs. See app.py for details.

In this case it is by adding a link with the character "é" so that when the link is clicked it sends a click webhook event with that character in the "url" value of the payload.

See the file send_message.py for the exact code and message.

Set up a basic web app to authenticate the payload and print out the response. Cause an "open" event that doesn't include the special character and and view the result. Cause a click event that includes the "é" character.

### Testing Creating the Signature Ourselves

Using the starkbank/ecdsa-python package that the SendGrid python package uses to verify the messages create a private and public key, then upload the public key to the server. Create payloads that match the passing and failing payloads from above. Create signatures, then send to the server using the updated public key.

Check the status of whether the webhooks are passing or failing.

## Results

### SendGrid  Webhook

The message that did not include the special character was correctly authenticated. The message that did include the special character was not authenticated.

Correctly authenticated message from logs

```
Payload: '[{"email":"rarabor719@threepp.com","event":"open","ip":"xxx.xxx.xxx.xxx","sg_content_type":"html","sg_event_id":"j0NhGx01TCimNpTmBEN0Yg","sg_message_id":"m7BqO7JsQ_Obv9nkaA-sCA.filterdrecv-77df4fc8dd-6h694-1-609974BE-A5.0","timestamp":1620669647,"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]'
Timestamp: '1620669672'
Signature: 'MEUCIQCfyuukiyRXu8tTY0dN+eiouJrJ+bj4t7iI0+wgvIY+xAIgIvu2VUmpDpt9hLiQ1ond6Wkv7wnsJifTJBdZO+O9iHY='
Authenticated: True
```

Falsely rejected message from logs

```
Payload: '[{"email":"rarabor719@threepp.com","event":"click","ip":"xxx.xxx.xxx.xxx","sg_event_id":"EEKhxyYSSjCQ4M92ZUTVtg","sg_message_id":"m7BqO7JsQ_Obv9nkaA-sCA.filterdrecv-77df4fc8dd-6h694-1-609974BE-A5.0","timestamp":1620669677,"url":"https://example.com?test=Daré","url_offset":{"index":0,"type":"html"},"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'
Timestamp: '1620669695'
Signature: 'MEUCIFxRxfMcENGrtAj0vAvmqix051ZIBFVHzCsWcFdZrUZ7AiEA5GzAOf5SlyN2Z+JW5jy+NZNAk67Nb0wQuGw+EYfmwkM='
Authenticated: False
```

### Creating the Signature Ourselves

When we signed the webhooks ourselves we were able to get both to pass, leading us to believe that our authentication on the server works correctly, and that the package can handle characters correctly. It leads us to believe something may be wrong with the signature we are receiving from SendGrid.

Correctly authenticated message from logs

```
Payload: '{"email":"rarabor719@threepp.com","event":"open","ip":"xxx.xxx.xxx.xxx","sg_content_type":"html","sg_event_id":"j0NhGx01TCimNpTmBEN0Yg","sg_message_id":"m7BqO7JsQ_Obv9nkaA-sCA.filterdrecv-77df4fc8dd-6h694-1-609974BE-A5.0","timestamp":1620669695,"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'
Timestamp: '1620669695'
Signature: 'MEUCIQCa5x3vlvFGntKqLJzlVhb1VtwF6pikj20PpOFCoZO00QIgKvus6SeZ7fmlNCBJ/h5pCcj2wBg2eUuWQN5dJ6vz/l0='
Authenticated: True
```

Correctly authenticated message from logs

```
Payload: '[{"email":"rarabor719@threepp.com","event":"click","ip":"xxx.xxx.xxx.xxx","sg_event_id":"EEKhxyYSSjCQ4M92ZUTVtg","sg_message_id":"m7BqO7JsQ_Obv9nkaA-sCA.filterdrecv-77df4fc8dd-6h694-1-609974BE-A5.0","timestamp":1620669695,"url":"https://example.com?test=Daré","url_offset":{"index":0,"type":"html"},"useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}]\r\n'
Timestamp: '1620669695'
Signature: 'MEUCIAj+j/LSJ8Lw9fZxXVog+bk4ydBycJAx9wGzZORuvDjyAiEAhulNXGqgoDGNc5i59a4mtt3GGPkDlMY6aA2n8K6ebCM='
Authenticated: True
```

## Required env vars

### App only (Heroku)

* PUBLIC_SENDGRID_KEY=key to authenticate messages
* PERSONAL_PUBLIC_SENDGRID_KEY=personal public key to check mock webhook endpoint

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
