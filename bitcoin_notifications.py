# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 18:27:50 2021

@author: @brianbrosky
"""

import requests
import time
from datetime import datetime
import settings
from os import environ
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint




BITCOIN_PRICE_THRESHOLD = 20000  # Set this to whatever you like

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', 
                               format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        # Sleep for 5 minutes 
        # (For testing purposes you can set it to a lower number)
        time.sleep(5 * 60)



def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)
    
API_KEY_COINMARKET = environ['API_KEY_COINMARKET']
    
BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
IFTT_KEY = environ['IFTTT_KEY']
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/'+IFTT_KEY


parameters = {
    'slug':'bitcoin',
    'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY_COINMARKET
}

session = Session()
session.headers.update(headers)



def get_latest_bitcoin_price():
    response = session.get(BITCOIN_API_URL, params=parameters)
    data = json.loads(response.text)
    # Convert the price to a floating point number
    return float(data['data']['1']['quote']['USD']['price'])


def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)


if __name__ == '__main__':
    main()