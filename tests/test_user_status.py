#!/usr/bin/env python3
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
def test_post_user_status_minimal(mock_requests, mock_info):
    mock_requests.post.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.post_user_status(
        username = "Max Mustermann",
        status = "coming"
    )

    mock_requests.post.assert_called_once_with(
        'https://connectapi.feuersoftware.com/interfaces/public/operation/userstatus',
        data='{"username": "Max Mustermann", "status": "coming"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})

    mock_info.assert_called_with("Success, API call 'post user status' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_post_user_status_full(mock_requests, mock_info):
    mock_requests.post.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.post_user_status(
        username = "Max Mustermann",
        status = "coming",
        operationid = 12345
    )

    mock_requests.post.assert_called_once_with(
        'https://connectapi.feuersoftware.com/interfaces/public/operation/userstatus',
        data='{'
             '"username": "Max Mustermann", '
             '"status": "coming", '
             '"operationid": 12345'
             '}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})

    mock_info.assert_called_with("Success, API call 'post user status' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.logging.Logger.warning")
@patch("feuersoftware.requests")
def test_post_user_status_invalid_arg(mock_requests, mock_warning, mock_info):
    mock_requests.post.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.post_user_status(
        username = "Max Mustermann",
        status = "coming",
        invalid_arg = "invalid"
    )

    mock_warning.assert_called_with('Invalid argument passed to post_user_status: invalid_arg=invalid')

    mock_requests.post.assert_called_once_with(
        'https://connectapi.feuersoftware.com/interfaces/public/operation/userstatus',
        data='{"username": "Max Mustermann", "status": "coming"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})

    mock_info.assert_called_with("Success, API call 'post user status' complete")

@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_post_user_status(mock_requests, mock_error):
    mock_requests.post.return_value.status_code = 401
    mock_requests.post.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    api.post_user_status(
        username = "Max Mustermann",
        status = "coming",
    )

    mock_error.assert_called_with("Error while sending API call 'post user status': 401 unauthorized")
