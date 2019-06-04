#!/bin/bash

cd tests/htmlcov

python -m http.server --bind 0.0.0.0 8090
