import os
from dotenv import load_dotenv

import pandas as pd
from orders import get_orders
from products import get_active_products


def main():

    # retrieve environment variables
    load_dotenv()
    secrets = {
        "SHOP_URL": os.getenv("SHOP_URL"),
        "API_VERSION": os.getenv("API_VERSION"),
        "PRIVATE_KEY": os.getenv("PRIVATE_KEY")
    }

    # define product fields to get
    product_fields = ["title", "variants"]
    # get products
    products = get_active_products(product_fields, secrets)
    # define order fields
    order_fields = ["id", "line_items"]
    # get orders
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
    df_products = df_products.set_axis(['product', 'quantity', 'times ordered'], axis=1, copy=False)
    df_products = df_products.fillna(0)

    # calculate average orders per day and days of stock remaining for each product variant
    days = 90
    restock_time = 25
    orders_per_day = []
    days_of_stock_remaining = []
    days_to_restock = []
    for index, row in df_products.iterrows():
        if row['times ordered'] != 0:
            average_orders_sold = row['times ordered'] / days
            orders_per_day.append(average_orders_sold)
            stock_remaining = round(row['quantity'] / average_orders_sold)
            days_of_stock_remaining.append(stock_remaining)
            days_to_restock.append(stock_remaining - restock_time)
        else:
            orders_per_day.append(0)
            days_of_stock_remaining.append("n/a")
            days_to_restock.append("n/a")

    # append to DataFrame
    df_products.insert(3, "orders per day", orders_per_day, allow_duplicates=True)
    df_products.insert(4, "days of stock remaining", days_of_stock_remaining, allow_duplicates=True)
    df_products.insert(5, "days to restock", days_to_restock, allow_duplicates=True)
    df_products = df_products.fillna(0)
    df_products.to_excel("output.xlsx")
    return df_products

if __name__ == "__main__":
    df = main()