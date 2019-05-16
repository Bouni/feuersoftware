#!/usr/bin/bash

version=$(egrep -o "([0-9]{1,}\.)+[0-9]{1,}" setup.py)

echo Current version is $version

echo Specify new version:

read newversion

echo New version will be $newversion

sed -i s/$version/$newversion/ setup.py


rm -rf build dist feuersoftware.egg-info

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*
