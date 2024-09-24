#!/bin/bash
pip install --target ./package -r requirements.txt
cd package
zip -r ../main.zip .
cd ..
zip -g main.zip src/main.py