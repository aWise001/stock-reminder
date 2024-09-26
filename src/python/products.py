import os

import requests


def get_active_products(field_list, secrets):

    shop_url = secrets["SHOP_URL"]
    api_version = secrets["API_VERSION"]
    private_key = secrets["PRIVATE_KEY"]

    headers = {
    "X-Shopify-Access-Token": private_key,
    "Content-Type": "application/json"
    }

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