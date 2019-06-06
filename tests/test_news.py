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
def test_get_news(mock_requests, mock_info):
    mock_requests.get.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.get_news()
    mock_requests.get.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news",
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'get news' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_get_news(mock_requests, mock_error):
    mock_requests.get.return_value.status_code = 401
    mock_requests.get.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    api.get_news()
    mock_error.assert_called_with("Error while sending API call 'get news': 401 unauthorized")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_minimal_post_news(mock_requests, mock_info):
    mock_requests.post.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.post_news(
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00")
    mock_requests.post.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news",
        data='{"title": "Test Title", "content": "Test Content", "start": "2019-06-01T12:00:00", "end": "2019-06-01T18:00:00"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'post news' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_full_post_news(mock_requests, mock_info):
    mock_requests.post.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.post_news(
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00",
        groups=["Kommandanten","Ausbilder"],
        mailinglists=["Kommando-ML","Ausbilder-ML"],
        site="Gerätehaus")
    mock_requests.post.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news",
        data='{'
             '"title": "Test Title", '
             '"content": "Test Content", '
             '"start": "2019-06-01T12:00:00", '
             '"end": "2019-06-01T18:00:00", '
             '"groups": ["Kommandanten", "Ausbilder"], '
             '"mailinglists": ["Kommando-ML", "Ausbilder-ML"], '
             '"site": "Ger\\u00e4tehaus"'
             '}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'post news' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.logging.Logger.warning")
@patch("feuersoftware.requests")
def test_invalid_arg_post_news(mock_requests, mock_warning, mock_info):
    mock_requests.post.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.post_news(
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00",
        invalid_arg="invalid")
    mock_warning.assert_called_with('Invalid argument passed to post_news: invalid_arg=invalid')
    mock_requests.post.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news",
        data='{"title": "Test Title", "content": "Test Content", "start": "2019-06-01T12:00:00", "end": "2019-06-01T18:00:00"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'post news' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_post_news(mock_requests, mock_error):
    mock_requests.post.return_value.status_code = 401
    mock_requests.post.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    api.post_news(
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00")
    mock_error.assert_called_with("Error while sending API call 'post news': 401 unauthorized")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_delete_news(mock_requests, mock_info):
    mock_requests.delete.return_value.status_code = 204
    api = PublicAPI(TOKEN)
    api.delete_news(1)
    mock_requests.delete.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news/1",
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'delete news' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_delete_news(mock_requests, mock_error):
    mock_requests.delete.return_value.status_code = 401
    mock_requests.delete.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    api.delete_news(1)
    mock_error.assert_called_with("Error while sending API call 'delete news': 401 unauthorized")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_minimal_put_news(mock_requests, mock_info):
    mock_requests.put.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.put_news(
        id=1,
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00")
    mock_requests.put.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news/1",
        data='{"title": "Test Title", "content": "Test Content", "start": "2019-06-01T12:00:00", "end": "2019-06-01T18:00:00"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'put news' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.requests")
def test_full_put_news(mock_requests, mock_info):
    mock_requests.put.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.put_news(
        id=1,
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00",
        groups=["Kommandanten","Ausbilder"],
        mailinglists=["Kommando-ML","Ausbilder-ML"],
        site="Gerätehaus")
    mock_requests.put.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news/1",
        data='{'
             '"title": "Test Title", '
             '"content": "Test Content", '
             '"start": "2019-06-01T12:00:00", '
             '"end": "2019-06-01T18:00:00", '
             '"groups": ["Kommandanten", "Ausbilder"], '
             '"mailinglists": ["Kommando-ML", "Ausbilder-ML"], '
             '"site": "Ger\\u00e4tehaus"'
             '}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'put news' complete")


@patch("feuersoftware.logging.Logger.info")
@patch("feuersoftware.logging.Logger.warning")
@patch("feuersoftware.requests")
def test_invalid_arg_put_news(mock_requests, mock_warning, mock_info):
    mock_requests.put.return_value.status_code = 200
    api = PublicAPI(TOKEN)
    api.put_news(
        id=1,
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00",
        invalid_arg="invalid")
    mock_warning.assert_called_with('Invalid argument passed to put_news: invalid_arg=invalid')
    mock_requests.put.assert_called_once_with(
        f"https://connectapi.feuersoftware.com/interfaces/public/news/1",
        data='{"title": "Test Title", "content": "Test Content", "start": "2019-06-01T12:00:00", "end": "2019-06-01T18:00:00"}',
        headers={"authorization": f"bearer {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"})
    mock_info.assert_called_with("Success, API call 'put news' complete")


@patch("feuersoftware.logging.Logger.error")
@patch("feuersoftware.requests")
def test_error_put_news(mock_requests, mock_error):
    mock_requests.put.return_value.status_code = 401
    mock_requests.put.return_value.text = "unauthorized"
    api = PublicAPI("ABCD")
    api.put_news(
        id=1,
        title="Test Title",
        content="Test Content",
        start="2019-06-01T12:00:00",
        end="2019-06-01T18:00:00")
    mock_error.assert_called_with("Error while sending API call 'put news': 401 unauthorized")
