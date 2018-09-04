# -*- coding: utf-8 -*-

import re
import logging
import requests
import voluptuous as vol

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("Feuersoftware API")

class PublicAPI(object):

    def __init__(self, token):
        self._headers = None
        vtoken = vol.Schema({vol.Required('token'): vol.All(str, vol.Length(560, 560, "Invalid length"))})
        self._headers = {
            'authorization': 'bearer {0}'.format(vtoken({"token":token}).get("token")),
            'accept': 'application/json',
            'content-type': 'application/json',
            }
        self._body = None
        self._url = None


    def operation(self, start, keyword, address=None, position=None, facts=None, ric=None, properties=None):
        if not self._headers:
            _LOGGER.error("Aborting, API not initialized")
            return 
        self._url = "https://connectapi.feuersoftware.com/interfaces/public/operation"
        data = []
        vstart = vol.Schema({vol.Required('start'): vol.All(str, vol.Match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "Not a ISO 8601 date"))})
        data.append(('start', vstart({"start":start}).get("start")))
        vkeyword = vol.Schema({vol.Required('keyword'): vol.All(str, vol.Length(1, 255, "Invalid length"))})
        data.append(('keyword', vkeyword({"keyword":keyword}).get("keyword")))
        
        if address:
            vaddress = vol.Schema({vol.Optional('address'): vol.All(str, vol.Length(1, 255, "Invalid length"))})
            try:
                data.append(('address', vaddress({"address":address}).get("address")))
            except Exception as e:
                _LOGGER.warning("Validation error: {0}. Ignoring argument.".format(e))
        if position:
            vposition = vol.Schema({vol.Optional('position'): vol.All(str, vol.Match(r"\d{1,3}\.\d+,\s?\d{1,3}\.\d+", "Not a valid WSG84 coordinate"))})
            try:
                data.append(('position', {k: float(v) for k, v in zip(["latitude","longitude"] ,vposition({"position":position}).get("position").replace(" ","").split(","))}))
            except Exception as e:
                _LOGGER.warning("Validation error: {0}. Ignoring argument.".format(e))
        if facts:
            vfacts = vol.Schema({vol.Optional('facts'): vol.All(str, vol.Length(1, 255, "Invalid length"))})
            try:
                data.append(('facts', vfacts({"facts":facts}).get("facts")))
            except Exception as e:
                _LOGGER.warning("Validation error: {0}. Ignoring argument.".format(e))
        if ric:
            vric = vol.Schema({vol.Optional('ric'): vol.All(str, vol.Length(1, 255, "Invalid length"))})
            try:
                data.append(('ric', vric({"ric":ric}).get("ric")))
            except Exception as e:
                _LOGGER.warning("Validation error: {0}. Ignoring argument.".format(e))
        if properties:
            _properties = []
            vproperties = vol.Schema({vol.Optional('properties'): list})
            try:
                vproperties({"properties": properties})
                vproperty = vol.Schema({
                        vol.Required('key'): vol.All(str, vol.Length(1, 255, "Invalid length")),
                        vol.Required('value'): vol.All(str, vol.Length(1, 255, "Invalid length")),
                        })
                for p in properties:
                    try:
                        _properties.append(vproperty(p))
                    except Exception as e:
                        _LOGGER.warning("Validation error: {0}. Ignoring argument.".format(e))
            except Exception as e:
                _LOGGER.warning("Validation error: {0}. Ignoring argument.".format(e))
            if _properties:
                data.append(('properties',_properties))

        self._body = {k: v for k, v in data}


    def vehicle_status(self, radioid, status, position=None):
        if not self._headers:
            _LOGGER.error("Aborting, API not initialized")
            return 
        data = []
        vradioid = vol.Schema({vol.Required('radioid'): vol.All(vol.Any(str,int), vol.Length(1, 255, "Invalid length"))})
        self._url = "https://connectapi.feuersoftware.com/interfaces/public/vehicle/{}/status".format(vradioid({"radioid":radioid}).get("radioid"))
        vstatus = vol.Schema({vol.Required('status'): vol.All(int, vol.Range(min=0, max=9))})
        data.append(('status', vstatus({"status":status}).get("status")))
        
        if position:
            vposition = vol.Schema({vol.Optional('position'): vol.All(str, vol.Match(r"\d{1,3}\.\d+,\s?\d{1,3}\.\d+", "Not a valid WSG84 coordinate"))})
            try:
                data.append(('position', {k: float(v) for k, v in zip(["latitude","longitude"] ,vposition({"position":position}).get("position").replace(" ","").split(","))}))
            except Exception as e:
                _LOGGER.warning("Validation error: {0}. Ignoring argument.".format(e))
        self._body = {k: v for k, v in data}
    

    def send(self):
        r = requests.post(self._url, data=json.dumps(self._body), headers=self._headers)
        if r.status_code != 200:
            _LOGGER.error("Error while sending API call: {0}".format(r.text))
        else:
            _LOGGER.info("Success, API call complete")

