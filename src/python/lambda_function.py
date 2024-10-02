import json
import os

import boto3
import pandas as pd
import requests
from orders import get_orders
from products import get_active_products


def lambda_handler(event, context):

    # get AWS secret containing shopify key
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    secrets_url = "http://localhost:2773/secretsmanager/get?secretId=shopify-API-key"
    r = requests.get(secrets_url, headers=headers)
    if r.status_code == 200:
        data = r.json()
    secrets = json.loads(data["SecretString"])

    # get products
    product_fields = ["id", "title", "status", "variants"]
    products = get_active_products(product_fields, secrets)

    # get orders
    order_fields = ["id", "created_at", "total_price", "number", "line_items"]
    orders = get_orders(order_fields, secrets)

    # populate series with product variant quantities
    product_quantities = {}
    for product in products['products']:
        for variant in product['variants']:
            if variant['inventory_quantity'] >= 0:
                product_variant = f"{product['title']} - {variant['title']}"
                product_quantities.update({product_variant: variant['inventory_quantity']})
    product_series = pd.Series(product_quantities)
    product_series = product_series.groupby(product_series.index).first()

    # find number of orders for each product in product_series
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

    # combine products and times ordered into DataFrame
    df_products = pd.DataFrame({'quantity': product_series, 'times_ordered': order_series})
    df_products = df_products.fillna(0)

    # calculate average orders per day and days of stock remaining for each product variant
    days = 193
    orders_per_day = []
    days_of_stock_remaining = []
    for index, row in df_products.iterrows():
        average_orders_sold = row['times_ordered'] / days
        orders_per_day.append(average_orders_sold)
        days_of_stock_remaining.append(row['quantity'] / average_orders_sold)

    # append to DataFrame
    df_products.insert(2, "orders_per_day", orders_per_day, allow_duplicates=True)
    df_products.insert(3, "days_of_stock_remaining", days_of_stock_remaining, allow_duplicates=True)
    df_products = df_products.fillna(0)

    # define email args
    sender = "stockreminderdomain.com"
    recipient = "axel.wise@ba.com"
    subject = "stock reminder - TEST!"

    # init client
    client = boto3.client('ses', region='eu-west-2')

    # send email
    response = client.send_email(
        Destination={
            'ToAddresses': [recipient]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': df_products.head()
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject
            },
        },
        Source=sender
    )

    return {
        'statusCode': 200,
        'body': json.dumps("Email Sent Successfully. MessageId is: " + response['MessageId'])
    }
