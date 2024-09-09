from dotenv import load_dotenv
import requests

import os

load_dotenv()

shop_url = os.getenv("SHOP_URL")
api_version = os.getenv("API_VER")
private_app_password = os.getenv("PRIVATE_KEY")


headers = {
    "X-Shopify-Access-Token": private_app_password,
    "Content-Type": "application/json"
}

def get_active_products(field_list):
    fields = ""
    for i in range(len(field_list)):
        if i == 0:
            fields += field_list[i]
        else:
            fields += f"%2C{field_list[i]}"
    endpoint = f"https://{shop_url}/admin/api/{api_version}/products.json?fields={fields}&limit=250&status=active"
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
    return data