#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import random
import string
import json
import pytest
import unittest
import requests
from mock import Mock, patch
from datetime import datetime as dt

sys.path.insert(0, os.path.abspath('./'))

from feuersoftware import PublicAPI



def randomToken(stringLength=560):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))



def test_missing_token():
    with pytest.raises(Exception):
        api = PublicAPI()

def test_token_set():
    token = randomToken()
    api = PublicAPI(token)
    assert token in api._headers["authorization"]

def test_operation_success():
    with patch.object(requests, 'post') as post_mock:
        token = randomToken()
        api = PublicAPI(token)
        data = {
            "start": dt.now().isoformat(),
            "keyword": "Brand 2",
            "status": "new",
            "alarm_enabled": True,
            "address": "Teststrasse 10, 12345 Musterstadt",
            "position": {"latitude":"47.592127", "longitude":"8.296870"},
            "facts":  "Küchenbrand",
            "ric": "12B",
            "number": 54321,
            "properties": [{"key":"Fettbrand","value":"Nein"},{"key":"Noch·Personen·im·Gebäude","value":"Ja"}]
        }
        update_strategy = "none"
        api.operation(
            data["start"],
            data["keyword"],
            data["status"],
            data["alarm_enabled"],
            data["address"],
            data["position"],
            data["facts"],
            data["ric"],
            data["number"],
            data["properties"],
            update_strategy)
        api.send()

        post_mock.assert_called_once_with(
                f"https://connectapi.feuersoftware.com/interfaces/public/operation?updateStrategy={update_strategy}", 
                data=json.dumps(data),
                headers={"authorization": f"bearer {token}", 
                 "accept": "application/json", 
                 "content-type": "application/json"})

def test_operation_missing_arguments():
    token = randomToken()
    api = PublicAPI(token)
    with pytest.raises(Exception):
        api.operation()

def test_vehicle_status():
    with patch.object(requests, 'post') as post_mock:
        token = randomToken()
        api = PublicAPI(token)
        radioid = 123456
        data = {
            "status": 2,
            "position": {"Latitude":"47.592127", "Longitude":"8.296870"},
        }
        api.vehicle_status(
            radioid,
            data["status"],
            data["position"])
        api.send()

        post_mock.assert_called_once_with(
                f"https://connectapi.feuersoftware.com/interfaces/public/vehicle/{radioid}/status", 
                data=json.dumps(data),
                headers={"authorization": f"bearer {token}", 
                 "accept": "application/json", 
                 "content-type": "application/json"})

def test_vehicle_status_missing_arguments():
    token = randomToken()
    api = PublicAPI(token)
    with pytest.raises(Exception):
        api.vehicle_status()

