#!/usr/bin/env python

import os
import time

from krakenex import API

# Warning! Set these correctly :)
CURRENCY_NAME = 'XETC'
TRADE_PAIR = 'XETCXXBT'

# Warning! Keep these secret :)
KRAKEN_API_KEY = ''
KRAKEN_API_SECRET = ''

assert KRAKEN_API_KEY and KRAKEN_API_SECRET and CURRENCY_NAME


class OrderExistsException(Exception):
    pass

class PlaceOrderException(Exception):
    pass


def log(msg):
    print('[{}] {}'.format(time.ctime(), msg))

def get_balance(kraken, name):
    balances = kraken.query_private('Balance')['result']
    return float(balances[name])

def check_for_open_orders(kraken, pair):
    orders = kraken.query_private('OpenOrders')['result']['open']
    for order in orders.values():
        if order['descr']['pair'] == pair:
            raise OrderExistsException

def open_order(kraken, pair, amount):
    resp = kraken.query_private('AddOrder', {
        'pair': pair,
        'volume': amount,
        'type': 'sell',
        'ordertype': 'market',
    })
    if resp['error']:
        raise PlaceOrderException(resp['error'])


if __name__ == '__main__':
    kraken = API(KRAKEN_API_KEY, KRAKEN_API_SECRET)
    log('Autosell started for {}'.format(CURRENCY_NAME))
    while True:
        try:
                balance = get_balance(kraken, CURRENCY_NAME)
                log('Current balance: {} {}'.format(balance, CURRENCY_NAME))
                if balance > 0:
                        log('Checking for open trades..')
                        try:
                                check_for_open_orders(kraken, TRADE_PAIR)
                                open_order(kraken, TRADE_PAIR, balance)
                        except OrderExistsException:
                                log('Account has open orders, will not create')
                        except PlaceOrderException as exp:
                                log('Failed to place order: {}'.format(exp))
                        else:
                                log('Sell order places for {} {}'.format(balance, CURRENCY_NAME))
        except:
                 time.sleep(1)


        time.sleep(60)
