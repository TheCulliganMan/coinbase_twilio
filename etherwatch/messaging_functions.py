# /usr/bin/env python
import time
import locale
import json

import requests
from slackclient import SlackClient

from etherwatch.config.api_keys import TWILIO_KEYS
from etherwatch.config.api_keys import SLACK_KEYS
from etherwatch.config.positions import POSITIONS


locale.setlocale( locale.LC_ALL, '' )

class MessagingFunctions:
    # Writing Functions
    @staticmethod
    def write_position_message(person_str, eth_price, sign, position):
        message = '{}: ETH2USD price {}, your position is {}{} USD'.format(
            person_str,
            locale.currency(eth_price, grouping=True),
            sign,
            locale.currency(position, grouping=True)
        )
        return message

    # Rest Clients
    @staticmethod
    def get_twilio_client():
        client = TwilioRestClient(
                    TWILIO_KEYS['twilio_account_sid'],
                    TWILIO_KEYS['twilio_auth_token']
                 )
        return client

    @staticmethod
    def get_slack_client():
        client = SlackClient(SLACK_KEYS['test-token'])
        return client

    # Notifications
    @staticmethod
    def sms_notify(person_str, message):
        for person_str in POSITIONS:
            phone_number = POSITIONS[person_str]['phone_number']
            client = MessagingFunctions.get_twilio_client()
            message = client.messages.create(
                to=phone_number,
                from_=TWILIO_KEYS['twillo_numbers'][0],
                body=message
            )
            time.sleep(1)

    @staticmethod
    def slack_token_api(person_str, message, channel='#positions'):
        client = MessagingFunctions.get_slack_client()
        client.api_call(
          "chat.postMessage",
          channel=channel,
          text=message
        )

    @staticmethod
    def slack_webhook(person_str, message, webhook):
        slack_data = {'text':message}
        response = requests.post(
            webhook,
            data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )

    @staticmethod
    def notify(person_str, message, slack=True, sms=False):

        if slack:
            MessagingFunctions.slack_webhook(
                person_str,
                message,
                SLACK_KEYS['webhook']
            )

        if sms:
            MessagingFunctions.ms_notify(person_str, message)
