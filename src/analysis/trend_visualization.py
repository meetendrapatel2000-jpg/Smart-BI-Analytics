import pandas as pd
import plotly.graph_objects as go

from database import engine


query = "SELECT * FROM orders"

df = pd.read_sql(query, engine)

df["order_date"] = pd.to_datetime(df["order_date"])

monthly_sales = (
    df.groupby(df["order_date"].dt.to_period("M"))
    .agg(
        revenue=("total_revenue", "sum"),
        profit=("total_profit", "sum")
    )
    .reset_index()
)

monthly_sales["order_date"] = monthly_sales["order_date"].astype(str)


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=monthly_sales["order_date"],
        y=monthly_sales["revenue"],
        mode="lines+markers",
        name="Revenue"
    )
)

fig.add_trace(
    go.Scatter(
        x=monthly_sales["order_date"],
        y=monthly_sales["profit"],
        mode="lines+markers",
        name="Profit"
    )
)

fig.update_layout(
    title="Monthly Revenue & Profit Trend",
    xaxis_title="Month",
    yaxis_title="Amount",
    template="plotly_white"
)

fig.show()