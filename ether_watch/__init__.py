# /usr/bin/env python

from ether_watch.ether_functions import EtherFunctions
from ether_watch.messaging_functions import MessagingFunctions
from ether_watch.db_functions import DatabaseFunctions

from ether_watch.config.positions import POSITIONS

def get_eth_price():
    return EtherFunctions.get_eth_exchange_usd()


def message_clients(eth_price):
    for person_str in POSITIONS:
        person = POSITIONS[person_str]
        position = EtherFunctions.get_positions(eth_price, person)
        sign = EtherFunctions.set_sign(position)
        message = MessagingFunctions.write_position_message(
                person_str,
                eth_price,
                sign,
                position
        )
        MessagingFunctions.notify(person_str, message)


def log_eth_price(eth_price):
    DatabaseFunctions.create_database()
    DatabaseFunctions.log_price_datetime(eth_price)


def main():
    eth_price = get_eth_price()
    log_eth_price(eth_price)
    message_clients(eth_price)


if __name__ == '__main__':
    main()
