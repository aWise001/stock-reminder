#!/bin/bash
pip install --target ./package -r src/requirements.txt
cd package
zip -r ../deployment_package.zip .
cd ..
zip -g deployment_package.zip src/lambda_function.py