# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 16:26:35 2021

@author: facts
"""

import settings
from os import environ
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint


API_KEY_COINMARKET = environ['IFTTT_KEY']
print(API_KEY_COINMARKET)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
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

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  pprint(data['data']['1']['quote']['USD']['price'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)