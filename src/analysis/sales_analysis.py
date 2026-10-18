import pandas as pd


def calculate_sales_summary(df):

    total_revenue = df["total_revenue"].sum()
    total_cost = df["total_cost"].sum()
    total_profit = df["total_profit"].sum()
    total_orders = df["order_id"].nunique()
    total_quantity = df["quantity"].sum()

    average_order_value = total_revenue / total_orders
    profit_margin = (total_profit / total_revenue) * 100

    summary = {
        "Total Revenue": total_revenue,
        "Total Cost": total_cost,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Total Quantity": total_quantity,
        "Average Order Value": average_order_value,
        "Profit Margin": profit_margin
    }

    return summary

from database import engine


query = "SELECT * FROM orders"

df = pd.read_sql(query, engine)

summary = calculate_sales_summary(df)

print("\nSales Summary")
print("-" * 30)

for key, value in summary.items():
    print(f"{key}: {value}")