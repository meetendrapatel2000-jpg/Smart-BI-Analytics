import pandas as pd

from database import engine


query = "SELECT * FROM orders"

df = pd.read_sql(query, engine)

df["order_date"] = pd.to_datetime(df["order_date"])

monthly_sales = (
    df.groupby(df["order_date"].dt.to_period("M"))
    .agg(
        revenue=("total_revenue", "sum"),
        cost=("total_cost", "sum"),
        profit=("total_profit", "sum"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)

monthly_sales["order_date"] = monthly_sales["order_date"].astype(str)

print("\nMonthly Sales Analysis")
print("-" * 40)
print(monthly_sales)