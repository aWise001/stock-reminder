from dotenv import load_dotenv
import requests

import os
import re

load_dotenv()

shop_url = os.getenv("SHOP_URL")
api_version = os.getenv("API_VER")
private_app_password = os.getenv("PRIVATE_KEY")

endpoint = f"https://{shop_url}/admin/api/{api_version}/orders.json?status=any"

headers = {
    "X-Shopify-Access-Token": private_app_password,
    "Content-Type": "application/json"
}

expr = 'https.+rel="next"'
next_page = True

while (next_page):
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for order in data['orders']:
            print(f"Order number: {order['number']} Created at: {order['created_at']} Total: £{order['total_price']}")
        header_link = response.headers['link']
        links = header_link.split(", ")
        for link in links:
            if (re.search('rel="next"', link)):
                endpoint = link[1:-13]
            else:
                if (len(links) == 1):
                    next_page = False
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        next_page = None