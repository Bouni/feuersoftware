#!/usr/bin/bash

rm -rf build dist feuersoftware.egg-info

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*
