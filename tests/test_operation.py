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
def test_minimal_post_operation(mock_requests, mock_info):
    mock_requests.post.return_value.status_code = 204
    api = PublicAPI(TOKEN)
    api.post_operation(
        start = "2019-06-01T12:00:00",
        keyword = "Brand 2")
    mock_requests.post.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/operation?updateStrategy=none",
        data='{'
             '"start": "2019-06-01T12:00:00", '
             '"keyword": "Brand 2"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'post operation' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_full_post_operation(mock_requests, mock_info):
    mock_requests.post.return_value.status_code = 204
    api = PublicAPI(TOKEN)
    api.post_operation(
        start = "2019-06-01T12:00:00",
        end = "2019-06-01T14:00:00",
        keyword = "Brand 2",
        update_strategy = "none",
        status = "new",
        alarmenabled = True,
        address = "Teststrasse 10, 12345 Musterstadt",
        position = {"latitude":"47.592127", "longitude":"8.296870"},
        facts =  "Küchenbrand",
        ric = "12B",
        number = 54321,
        properties = [
            {"key":"Fettbrand","value":"Nein"},
            {"key":"Noch·Personen·im·Gebäude","value":"Ja"}])
    mock_requests.post.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/operation?updateStrategy=none",
        data='{'
             '"start": "2019-06-01T12:00:00", '
             '"keyword": "Brand 2", '
             '"end": "2019-06-01T14:00:00", '
             '"status": "new", '
             '"alarmenabled": true, '
             '"address": "Teststrasse 10, 12345 Musterstadt", '
             '"position": {"latitude": "47.592127", "longitude": "8.296870"}, '
             '"facts": "K\\u00fcchenbrand", '
             '"ric": "12B", '
             '"number": 54321, '
             '"properties": ['
                '{"key": "Fettbrand", "value": "Nein"}, '
                '{"key": "Noch\\u00b7Personen\\u00b7im\\u00b7Geb\\u00e4ude", "value": "Ja"}'
             ']}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'post operation' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.logging.Logger.warning")
@patch("feuersoftware.requests")
def test_invalid_arg_post_operation(mock_requests, mock_warning, mock_info):
    mock_requests.post.return_value.status_code = 204
    api = PublicAPI(TOKEN)
    api.post_operation(
        start = "2019-06-01T12:00:00",
        keyword = "Brand 2",
        invalid_arg = "invalid")
    mock_warning.assert_called_with('Invalid argument passed to post_operation: invalid_arg=invalid')
    mock_requests.post.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/operation?updateStrategy=none",
        data='{'
             '"start": "2019-06-01T12:00:00", '
             '"keyword": "Brand 2"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'post operation' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_post_operation(mock_requests, mock_error):
    mock_requests.post.return_value.status_code = 401
    mock_requests.post.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    api.post_operation(
        start = "2019-06-01T12:00:00",
        keyword = "Brand 2")
    mock_error.assert_called_with("Error while sending API call 'post operation': 401 unauthorized")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_get_operation(mock_requests, mock_info):
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.text = "[]"
    api = PublicAPI(TOKEN)
    r = api.get_operation()
    mock_requests.get.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/operation",
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'get operation' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_get_operation(mock_requests, mock_error):
    mock_requests.get.return_value.status_code = 401
    mock_requests.get.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    r = api.get_operation()
    mock_error.assert_called_with("Error while sending API call 'get operation': 401 unauthorized")
