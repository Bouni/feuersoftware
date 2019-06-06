#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import pytest

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


def test_missing_token():
    with pytest.raises(Exception):
        api = PublicAPI()

def test_token_set():
    api = PublicAPI(TOKEN)
    assert TOKEN in api._headers["authorization"]
