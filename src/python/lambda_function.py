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
            if variant['inventory_quantity'] > 0:
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
    df_products = pd.concat([product_series, order_series], axis=1).reset_index()
    df_products.set_axis(['product', 'quantity', 'times ordered'], axis=1, copy=False)
    df_products = df_products.fillna(0)

    # calculate average orders per day and days of stock remaining for each product variant
    days = 30
    restock_time = 25
    orders_per_day = []
    days_of_stock_remaining = []
    days_to_restock = []
    for index, row in df_products.iterrows():
        if row['times ordered'] != 0:
            average_orders_sold = row['times ordered'] / days
            orders_per_day.append(average_orders_sold)
            days_of_stock_remaining.append(row['quantity'] / average_orders_sold)
            days_to_restock.append(days_of_stock_remaining[-1] - restock_time)
        else:
            orders_per_day.append(0)
            days_of_stock_remaining.append("n/a")
            days_to_restock.append("n/a")

    # append to DataFrame
    df_products.insert(3, "orders per day", orders_per_day, allow_duplicates=True)
    df_products.insert(4, "days of stock remaining", days_of_stock_remaining, allow_duplicates=True)
    df_products.insert(5, "days to restock", days_to_restock, allow_duplicates=True)
    df_products = df_products.fillna(0)

    # create list of products with less than 5 days of stock remaining minus restock time
    restock_list = []
    for index, row in df_products.iterrows():
        if row['days to restock'] != "n/a" and row['days to restock'] <= 5:
            restock_list.append([row['product'], row['days to restock']])

    # define email args
    sender = "automatedreminder@stockreminderdomain.com"
    recipients = ["info@yijiu.store", "axelwise676@gmail.com"]
    subject = "stock reminder - TEST"
    body = "This is a test email sent from an automated lambda function,\n\n"
    # body += df_products.head().to_string()
    for i in restock_list:
        body += f"product: {i[0]}, days to restock: {i[1]}\n"

    # init client
    client = boto3.client('ses', region_name='eu-west-2')

    # send email
    response = client.send_email(
        Destination={
            'ToAddresses': [recipients[1]]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body
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
