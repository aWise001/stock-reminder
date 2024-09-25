import main
import requests
import json
import os

def lambda_handler(event, context):
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    secrets_url = "http://localhost:2773/secretsmanager/get?secretId=test-secret"
    r = requests.get(secrets_url, headers=headers)
    secret = json.loads(r.text)["SecretString"]
    # df = main.main()
    return secret