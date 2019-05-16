# -*- coding: utf-8 -*-

import re
import json
import logging
import requests

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("Feuersoftware API")

class PublicAPI(object):

    def __init__(self, token):
        self._headers = None
        self._headers = {
            'authorization': 'bearer {0}'.format(token),
            'accept': 'application/json',
            'content-type': 'application/json',
            }
        self._body = None
        self._url = None


    def operation(self, start, keyword, status='new',
                  alarm_enabled=True, address=None, position=None,
                  facts=None, ric=None, number=None, properties=None,
                  update_strategy='none'):
        self._body = None
        if not self._headers:
            _LOGGER.error("Aborting, API not initialized")
            return
        self._url = f"https://connectapi.feuersoftware.com/interfaces/public/operation?updateStrategy={update_strategy}"
        data = {}
        data['start'] = start
        data['keyword'] = keyword
        if status:
            data['status'] = status
        if alarm_enabled:
            data['alarm_enabled'] = alarm_enabled
        if address:
            data['address'] = address
        if position:
            data['position'] = position
        if facts:
            data['facts'] = facts
        if ric:
            data['ric'] = ric
        if number:
            data['number'] = number
        if properties:
            data['properties'] = properties
        self._body = data


    def vehicle_status(self, radioid, status, position=None):
        self._body = None
        if not self._headers:
            _LOGGER.error("Aborting, API not initialized")
            return
        self._url = "https://connectapi.feuersoftware.com/interfaces/public/vehicle/{}/status".format(radioid)
        data = {}
        data['status'] = status
        if position:
            data['position'] = position
        self._body = data


    def send(self):
        if self._body and self._headers and self._url:
            r = requests.post(self._url, data=json.dumps(self._body), headers=self._headers)
            if r.status_code != 200:
                _LOGGER.error("Error while sending API call: {0} {1}".format(r.status_text, r.text))
            else:
                _LOGGER.info("Success, API call complete")
            return r
        return
