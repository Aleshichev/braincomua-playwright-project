import logging

import pandas as pd
from parser_app.models import Product


def save_to_database(product_data: dict):
    """
    Save product data to the database.
    """
    try:
        product = Product.objects.create(**product_data)
        logging.info(f"Product saved to database with ID: {product.id}")
    except Exception as e:
        logging.error(f"Failed to save product to database: {e}")


def export_to_csv():
    """Export all products from the database to a CSV file."""
    try:
        products = Product.objects.all()
        if not products.exists():
            logging.warning("No products found in database to export")
            return

        df = pd.DataFrame(list(products.values()))
        df.to_csv("results/products.csv", index=False)
        logging.info(f"Successfully exported {len(df)} products to CSV")
    except Exception as e:
        logging.error(f"Failed to export products to CSV: {e}")