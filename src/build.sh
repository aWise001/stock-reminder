#!/bin/bash
pip install --target ./package -r requirements.txt
cd package
zip -r ../main.zip .
cd ../python
zip -g main.zip main.py