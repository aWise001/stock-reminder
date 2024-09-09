import numpy as np
import pandas as pd

from orders import get_orders, get_single_order
from products import get_active_products

def main():
    # define product fields to get
    product_fields = ["id", "title", "status", "variants"]
    # get products
    products = get_active_products(product_fields)
    # define order fields
    order_fields = ["id", "created_at", "total_price", "number", "line_items"]
    # get orders
    orders = get_orders(order_fields)

    product_quantities = {}
    for product in products['products']:
        for variant in product['variants']:
            product_variant = f"{product['title']} - {variant['title']}"
            product_quantities.update({product_variant: variant['inventory_quantity']})
    product_series = pd.Series(product_quantities)

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
    print(df_products.to_string())


if __name__ == "__main__":
    main()