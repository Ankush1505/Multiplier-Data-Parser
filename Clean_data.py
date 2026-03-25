import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "data"/"raw"
PROCESSED_DATA_DIR = BASE_DIR / "data"/"processed"


PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def clean_customers():
    file_path = RAW_DATA_DIR / "customers.csv"
    
    try:
        df = pd.read_csv(file_path)
        print("---Original Customers Data---")
        print(df.head(10))
        
        df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
        if df["signup_date"].isna().any():
            print("Warning: Unparseable dates found. Replaced with Nat(Not a time)")
            
        
        df = df.sort_values(by='signup_date', ascending=False)
        df = df.drop_duplicates(subset=['customer_id'], keep="first")
        
        
        df['name'] = df['name'].str.strip()
        df['region'] = df['region'].str.strip()
        df['region'] = df['region'].fillna('Unknown')
        df['email'] = df['email'].str.lower()
        df['valid_email'] = df['email'].notna() & df['email'].str.contains('@', na=False) & df['email'].str.contains('\.', na=False)

        print('---Cleaned_data---')
        print(df)

        clean_file = PROCESSED_DATA_DIR / 'customers_clean.csv'

        df.to_csv(clean_file, index=False)

        return df
    
    except Exception as e: 
        print(f"Error : {e}")
        return None


def parse_mixed_dates(date_val):
    
    for fmt in ('%Y-%m-%d', '%m-%d-%Y', '%d-%m-%Y'):
        try: 
            return pd.to_datetime(date_val, format=fmt)
        
        except (ValueError, TypeError):
            continue
        
    return pd.NaT

def clean_orders():
    file_path = RAW_DATA_DIR / "orders.csv"

    try:
       df =pd.read_csv(file_path)
       print("__Original Orders Data__")
       print(df.head(10))

       df['order_date'] = df['order_date'].apply(parse_mixed_dates)
       df = df.dropna(subset=["customer_id", "order_id"], how='all')
       df['amount'] = df.groupby("product_id")["amount"].transform(lambda x: x.fillna(x.median()))
       df['status'] = df['status'].str.lower().str.strip()

       status_mapping = {"done" : "completed", "canceled" : "cancelled"}
       df['status'] = df['status'].replace(status_mapping)

       df['order_year_month'] = df['order_date'].dt.strftime('%Y-%m')

       clean_file = PROCESSED_DATA_DIR / 'orders_clean.csv'

       df.to_csv(clean_file, index=False)
       print(f"Succefully saved Orders Clean file to {clean_file}")
       return df
    
    except Exception as e:
        print(f"Warning Errors in orders : {e}")
        return None

if __name__ == "__main__":
    clean_customers()
    clean_orders()