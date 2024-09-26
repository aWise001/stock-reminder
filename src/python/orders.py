import os
import re

import requests

created_at_min = "2024-03-01"

def get_orders(field_list, secrets):

    shop_url = secrets["SHOP_URL"]
    api_version = secrets["API_VERSION"]
    private_key = secrets["PRIVATE_KEY"]

    # define header
    headers = {
        "X-Shopify-Access-Token": private_key,
        "Content-Type": "application/json"
    }

    # create field string and add ASCII code for comma in between fields
    fields = ""
    for i in range(len(field_list)):
        if i == 0:
            fields += field_list[i]
        else:
            fields += f"%2C{field_list[i]}"
    # build endpoint link
    endpoint = f"https://{shop_url}/admin/api/{api_version}/orders.json?created_at_min={created_at_min}&fields={fields}&limit=250&status=any"
    # make API call
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
    next_page = True
    # get header link for next page
    link = response.headers['link']
    while next_page:
        # get next page link
        endpoint = get_next_page(link)
        if endpoint == None:
            break
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            new_orders = response.json()
            data['orders'] += new_orders['orders']
            # set next link
            link = response.headers['link']
        else:
            next_page = False
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    return data


def get_next_page(header_link):
    links = header_link.split(", ")
    next_page_link = None
    for link in links:
        if re.search('rel="next"', link):
            next_page_link = link[1:-13]
    return next_page_link



def get_single_order(order_ID, field_list):
    fields = ""
    for i in range(len(field_list)):
        if i == 0:
            fields += field_list[i]
        else:
            fields += f"%2C{field_list[i]}"

    endpoint = f"https://{shop_url}/admin/api/{api_version}/orders/{order_ID}.json?fields={fields}"

    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

    return data