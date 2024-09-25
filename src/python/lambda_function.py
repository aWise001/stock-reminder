import main
import requests
import json
import os

def lambda_handler(event, context):
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    
    df = main.main()
    return df