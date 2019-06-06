#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import pytest
from mock import patch

sys.path.insert(0, os.path.abspath('./'))

from feuersoftware import PublicAPI

TOKEN = '2xgRoQfoMGb4IveCDJIZqOO1l8hZZ5jT5mAw7SSk1otrFSq50IA2HIYB3luEpv7Vw8BWwG'\
        'Y2zV96VUkOF3FCZs2OP03qaTWF3CDrUHOKndvLIFTTgx0FCMBTFBRF1DfG4g3rs8BSMHB4'\
        '6qph1AlxOZ6parmJlp90V3GQB4EoI6DFdKE4SZeBuu46mXoaDlSmpTTS3FCpeG7oEUJVgy'\
        'pLZkZSFPRng5HdKhp6HG2XmNIMAtKTG3DAUWuKRi3cZ4JstLj05y4r7jt81g4DYXz9gVYc'\
        'UWk2pOkIZ9RPmu0s4LlaXHEK3TJlxLIUt5eHIzPUVKXyhdJDckviPsTYNfRxkpcNGd0vAb'\
        'zfzwMadgb4xaOi1v6ZpsRfXyOPgpudcnO6rwwi9TlAWNZ2075CO7HVFEP31yGhXmYsdFwj'\
        'ne3UIraWovMWHqeyv2yQLigKLePDAgXYUFqQpZ9P5ScznSMUg0ZnxS0Miy0qKe9zDYtqTk'\
        'qQVwrUGfGVFp4Ti83NJLCCGUOCmF0ovOB28mYyQIqGAi2MDaNIuAvz6HT1tGAo5nYdzOeu'


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_get_alarmgroup(mock_requests, mock_info):
    mock_requests.get.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.get_alarmgroup()
    mock_requests.get.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/alarmgroup",
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'get alarmgroup' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_get_alarmgroup(mock_requests, mock_error):
    mock_requests.get.return_value.status_code = 401
    mock_requests.get.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    api.get_alarmgroup()
    mock_error.assert_called_with("Error while sending API call 'get alarmgroup': 401 unauthorized")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_minimal_put_alarmgroup(mock_requests, mock_info):
    mock_requests.put.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.put_alarmgroup(1, "Test Gruppe", [{"id":1},{"id":2}])
    mock_requests.put.assert_called_once_with(
        "https://connectapi.feuersoftware.com/interfaces/public/alarmgroup/1",
        data='{"id": 1, "name": "Test Gruppe", "users": [{"id": 1}, {"id": 2}]}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'put alarmgroup' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_full_put_alarmgroup(mock_requests, mock_info):
    mock_requests.put.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    users = [{"id":1,
              "firstname": "Hans",
              "lastname": "Maier",
              "email": "hans.maier@ffw.de"},
            {"id":2,
             "firstname": "Bernd",
             "lastname": "Brot",
             "email": "bernd.das.brot@ffw.de"}]
    api.put_alarmgroup(1, "Test Gruppe", users)
    mock_requests.put.assert_called_once_with(
        "https://connectapi.feuersoftware.com/interfaces/public/alarmgroup/1",
        data='{'
             '"id": 1, '
             '"name": "Test Gruppe", '
             '"users": ['
             '{"id": 1, "firstname": "Hans", "lastname": "Maier", "email": "hans.maier@ffw.de"}, '
             '{"id": 2, "firstname": "Bernd", "lastname": "Brot", "email": "bernd.das.brot@ffw.de"}'
             ']}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'put alarmgroup' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_put_alarmgroup(mock_requests, mock_error):
    mock_requests.put.return_value.status_code = 401
    mock_requests.put.return_value.text = "unauthorized"
    api = PublicAPI(TOKEN)
    api.put_alarmgroup(1, "Test Gruppe", [{"id":1},{"id":2}])
    mock_error.assert_called_with("Error while sending API call 'put alarmgroup': 401 unauthorized")
