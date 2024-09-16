#!/bin/bash
pip install --target ./package -r src/requirements.txt
cd package
zip -r ../lambda_function.zip .
cd ..
zip -g lambda_function.zip src/lambda_function.py