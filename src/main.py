import numpy as np
import pandas as pd

from orders import get_orders
from products import get_active_products

def main():
    # define product fields to get
    product_fields = ["id", "title", "status"]
    # get products
    products = get_active_products(product_fields)
    # define order fields
    order_fields = ["id", "created_at", "total_price", "number", "line_items"]
    # get orders
    orders = get_orders(order_fields)

    for i in range(len(orders['orders'])):
        print(orders['orders'][i], i, "\n")

    # for i in range(len(products['products'])):
    #     print(products['products'][i], i)

if __name__ == "__main__":
    main()