import shopify
from dotenv import load_dotenv

import json
import os

load_dotenv()

shop_url = os.getenv("SHOP_URL")
api_version = os.getenv("API_VER")
private_app_password = os.getenv("PRIVATE_KEY")

session = shopify.Session(shop_url, api_version, private_app_password)

shopify.ShopifyResource.activate_session(session)

path = 'query.graphql'
with open(path, 'r') as file:
    file_content = file.read()

result = shopify.GraphQL().execute(file_content)
result_json = json.loads(result)
print(result_json['data']['products'])

shopify.ShopifyResource.clear_session()