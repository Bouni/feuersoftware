#!/usr/bin/env python3
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


    def post_operation(self, start, keyword, update_strategy='none', **kwargs):
        """Start, update, cancel or close an operation. https://connectapi.feuersoftware.com/swagger/ui/index#!/Public32API/Public_PostOperation"""
        self._url = "https://connectapi.feuersoftware.com/interfaces/public/operation?updateStrategy={0}".format(update_strategy)
        valid_args = ("end", "status", "alarm_enabled", "address", "position", "facts", "ric", "number", "properties")
        data = {"start": start, "keyword": keyword}
        for k, v in kwargs.items():
            if k in valid_args:
                data[k] = v
            else:
                _LOGGER.warning("Invalid argument passed to post_operation: {0}={1}".format(k, v))
        r = requests.post(self._url, data=json.dumps(data), headers=self._headers)
        if r.status_code != 204:
            _LOGGER.error("Error while sending API call 'post operation': {0} {1}".format(r.status_code, r.text))
        else:
            _LOGGER.info("Success, API call 'post operation' complete")
        return r


    def post_vehicle_status(self, radioid, status, **kwargs):
        self._url = "https://connectapi.feuersoftware.com/interfaces/public/vehicle/{0}/status".format(radioid)
        valid_args = ("position")
        data = {"status": status}
        for k, v in kwargs.items():
            if k in valid_args:
                data[k] = v
            else:
                _LOGGER.warning("Invalid argument passed to post_vehicle_status: {0}={1}".format(k, v))
        r = requests.post(self._url, data=json.dumps(data), headers=self._headers)
        if r.status_code != 204:
            _LOGGER.error("Error while sending API call 'post vehicle status': {0} {1}".format(r.status_code, r.text))
        else:
            _LOGGER.info("Success, API call 'post vehicle status' complete")
        return r
