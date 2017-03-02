# /usr/bin/env python

# Standard library
import datetime
import locale
import sqlite3
import time

# Third party
from coinbase.wallet.client import Client as CoinbaseClient
from twilio.rest import TwilioRestClient

# project
from coinbase_twilio.config.api_keys import COINBASE_KEYS
from coinbase_twilio.config.api_keys import TWILIO_KEYS
from coinbase_twilio.config.api_keys import TWILIO_NUMBER
from coinbase_twilio.config.positions import POSITIONS

locale.setlocale( locale.LC_ALL, '' )

# Database
def create_database(db='ether.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ether
         (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, price real)''')
    c.close()

def log_price_datetime(price, db='ether.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('INSERT INTO ether (price) VALUES (?)',  (price,) )
    conn.commit()
    c.close()

def get_price_log(db='ether.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for row in c.execute('SELECT * FROM ether'):
        print(row)
    c.close()

# Rest Clients
def get_twilio_client():
    client = TwilioRestClient(
                TWILIO_KEYS['twilio_account_sid'],
                TWILIO_KEYS['twilio_auth_token']
             )
    return client


def get_coinbase_client():
    client = CoinbaseClient(
                COINBASE_KEYS['api_key'],
                COINBASE_KEYS['api_secret']
             )
    return client

# Notifications
def sms_notify(message, phone_number):
    client = get_twilio_client()
    message = client.messages.create(
        to=phone_number,
        from_=TWILIO_NUMBER,
        body=message
    )

def price_correct(price):
    return (price + (price * 0.0149))

def get_positions(eth_price, person):
    co_position = (eth_price - price_correct(person['price']))
    gross_position = co_position * person['quantity']
    return gross_position

# Coinbase
def get_eth_exchange(curr_string='USD'):
    client = get_coinbase_client()
    #print(client.get_buy_price())
    eth_exchange_rates = client.get_exchange_rates(currency='ETH')['rates']
    eth_to_usd = eth_exchange_rates['USD']
    return float(eth_to_usd)

def get_eth_exchange_usd():
    return get_eth_exchange()

def get_eth_exchange_btc():
    return get_eth_exchange('BTC')

def set_sign(position):
    if position >= 0:
        sign = "+"
    else:
        sign = "-"
    return sign

def log_positions_text_clients():
    create_database()
    eth_price = get_eth_exchange_usd()
    log_price_datetime(eth_price)
    get_price_log()

    for person_str in POSITIONS:
        time.sleep(1.1)
        person = POSITIONS[person_str]
        position = get_positions(eth_price, person)

        sign = set_sign(position)

        message = 'ETH2USD price {}, your position is {}{} USD'.format(
            locale.currency(eth_price, grouping=True),
            sign,
            locale.currency(position, grouping=True)
        )

        sms_notify(message, person['phone_number'])

def main():
    log_positions_text_clients()

if __name__ == '__main__':
    main()
