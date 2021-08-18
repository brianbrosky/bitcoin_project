# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 17:11:13 2021

@author: facts
"""
import settings
from os import environ
import requests


IFTT_KEY = environ['IFTTT_KEY']


ifttt_webhook_url = 'https://maker.ifttt.com/trigger/test_event/with/key/' + IFTT_KEY
requests.post(ifttt_webhook_url)