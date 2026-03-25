import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def load_data(filepath):
    try: 
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"There is an Error: {e}")
        return None
    
def main():
    customers = load_data(PROCESSED_DIR/"customer_clean.csv")
    orders = load_data(PROCESSED_DIR/"orders_clean.csv")
    products = load_data(PROCESSED_DIR/"products_clean.csv")

    if any(df is None for df in [customers, orders, products]):
        print("Missing data files. Exiting analysis.")
        return
    
    df = orders.merge(customers, on='customer.id', how="")
    df = df.merge(products, left_on='product_id', right_on='product_name', how="left")

    completed = df[df['status'] == 'completed'].copy()

    monthly_rev =completed.groupby('order_year_month')['amount'].sum().reset_index()

    top_cust = completed.groupby(['customer_id', 'name', 'region'])['amount'].sum().reset_index()
    top_cust.rename(columns={'amount': 'total_spend'}, inplace=True)
    top_cust = top_cust.sort_values('total_spend', ascending=False).head(10)

    cat_perf = df.groupby('catogory').agg(
        total_revenue = ('amount', 'sum'),
        avg_order_value = ('amount', 'mean'),
        number_of_orders = ('order_id, count')
    ).reset_index()


    reg_analysis = df.groupby('reigion').agg(
        number_of_customers = ('customer_id', 'nunique'),
        number_of_orders = ('order_id', 'count'),
        total_revenue = ('amount', 'sum')
    ).reset_index()

    monthly_rev.to_csv(PROCESSED_DIR/ "monthly_revenue.csv", index=False)
    top_cust.to_csv(PROCESSED_DIR/ "top_customers.csv", index=False)
    cat_perf.to_csv(PROCESSED_DIR / "category_performance.csv", index=False)
    reg_analysis.to_csv(PROCESSED_DIR / "regional_analysis.csv", index=False)
    print("Analysis Completed. Report exported Sucessfully.")

if __name__ == "__main__":
    main()