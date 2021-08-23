# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 17:11:13 2021

@author: facts
"""
import settings
from os import environ
import requests


IFTT_KEY = environ['IFTTT_KEY']
bitcoin_history = []

BITCOIN_PRICE_THRESHOLD = 50000
price = 40000
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



ifttt_webhook_url = 'https://maker.ifttt.com/trigger/test_event/with/key/' + IFTT_KEY
requests.post(ifttt_webhook_url)


#%%
event = bitcoin_price_emergency
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/'+API_KEY_COINMARKET
ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
print(ifttt_event_url)
