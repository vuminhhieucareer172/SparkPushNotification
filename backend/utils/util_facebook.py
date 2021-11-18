from flask import request

import requests
import json


def call_send_api(senderPsid, response):
    PAGE_ACCESS_TOKEN = ''

    payload = {
        'recipient': {
            'id': senderPsid
        },
        'message': response,
        'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}

    url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)


def handle_message(senderPsid, receivedMessage):
    if 'text' in receivedMessage:

        response = {"text": 'Your PSID is: {}'.format(senderPsid)}

        call_send_api(senderPsid, response)
    else:
        response = {"text": 'This chatbot only accepts text messages'}
        call_send_api(senderPsid, response)


def webhook():
    if request.method == 'GET':
        # do something.....
        VERIFY_TOKEN = "128fea16-bef2-4f86-8402-2fbb9b9ed70e"

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        return 'SOMETHING', 200

    if request.method == 'POST':
        VERIFY_TOKEN = "128fea16-bef2-4f86-8402-2fbb9b9ed70e"

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        data = request.data
        body = json.loads(data.decode('utf-8'))

        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))
                if 'message' in webhookEvent:
                    handle_message(senderPsid, webhookEvent['message'])

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404
