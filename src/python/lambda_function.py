import os

import pandas as pd
import requests
from orders import get_orders
from products import get_active_products


def lambda_handler(event, context):

    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    secrets_url = "http://localhost:2773/secretsmanager/get?secretId=shopify-API-key"
    r = requests.get(secrets_url, headers=headers)
    if r.status_code == 200:
        data = r.json()
    secrets = data["SecretString"]

    # define product fields to get
    product_fields = ["id", "title", "status", "variants"]
    # get products
    products = get_active_products(product_fields, secrets)
    # define order fields
    order_fields = ["id", "created_at", "total_price", "number", "line_items"]
    # get orders
    orders = get_orders(order_fields, secrets)

    product_quantities = {}
    for product in products['products']:
        for variant in product['variants']:
            if variant['inventory_quantity'] >= 0:
                product_variant = f"{product['title']} - {variant['title']}"
                product_quantities.update({product_variant: variant['inventory_quantity']})
    product_series = pd.Series(product_quantities)
    product_series = product_series.groupby(product_series.index).first()

    times_ordered = {}
    for order in orders['orders']:
        for item in order['line_items']:
            item_name = item['name']
            if item_name in product_series.index:
                if item_name in times_ordered:
                    times_ordered[item_name] += 1
                else:
                    times_ordered[item_name] = 1
    order_series = pd.Series(times_ordered)

    df_products = pd.DataFrame({'quantity': product_series, 'times_ordered': order_series})
    df_products = df_products.fillna(0)

    days = 193
    orders_per_day = []
    days_of_stock_remaining = []
    for index, row in df_products.iterrows():
        average_orders_sold = row['times_ordered'] / days
        orders_per_day.append(average_orders_sold)
        days_of_stock_remaining.append(row['quantity'] / average_orders_sold)

    df_products.insert(2, "orders_per_day", orders_per_day, allow_duplicates=True)
    df_products.insert(3, "days_of_stock_remaining", days_of_stock_remaining, allow_duplicates=True)
    df_products = df_products.fillna(0)

    return secrets
