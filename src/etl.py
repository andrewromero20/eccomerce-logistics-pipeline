import os
import pandas as pd
from sqlalchemy import create_engine, inspect

# 1. Paths configuration and database engine setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "olist.db")

# Create connection to SQLite using SQLAlchemy
engine = create_engine(f"sqlite:///{DB_PATH}")

# Mapping of CSV files to SQL table names
DATASETS = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

def load_data_to_sqlite():
    print("Starting ETL Process...")
    
    for table_name, csv_filename in DATASETS.items():
        csv_path = os.path.join(RAW_DATA_DIR, csv_filename)
        
        if not os.path.exists(csv_path):
            print(f" Warning: File not found {csv_filename}")
            continue
            
        print(f"Loading {csv_filename} -> Table '{table_name}'...")
        
        # Leer CSV en Pandas
        df = pd.read_csv(csv_path)
        
        # Guardar como tabla en SQLite
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"  Table '{table_name}' loaded with {len(df):,} rows.")
        
    print("\n🔍 Verifying tables in the Database...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"🎉 Tables completed. Tables in 'olist.db': {tables}")

if __name__ == "__main__":
    load_data_to_sqlite() 
