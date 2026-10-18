import streamlit as st
import pandas as pd
from src.database import engine

st.set_page_config(
    page_title="Smart BI Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart Data Analytics & Business Intelligence")
st.write("Executive Dashboard")

st.sidebar.header("🎛️ Dashboard Filters")

region_query = """
SELECT region_id, region_name
FROM regions
ORDER BY region_id
"""

region_filter_data = pd.read_sql(
    region_query,
    engine
)

regions = ["All"] + region_filter_data["region_name"].tolist()

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

category_filter_query = """
SELECT DISTINCT c.category_name
FROM categories c
ORDER BY c.category_name
"""

category_filter_data = pd.read_sql(
    category_filter_query,
    engine
)

categories = ["All"] + category_filter_data["category_name"].tolist()

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

query = "SELECT * FROM orders"

df = pd.read_sql(query, engine)

if selected_region != "All":

    selected_region_id = region_filter_data[
        region_filter_data["region_name"] == selected_region
    ]["region_id"].iloc[0]

    df = df[
        df["region_id"] == selected_region_id
    ]


if selected_category != "All":

    category_map_query = """
    SELECT
        p.product_id,
        c.category_name
    FROM products p
    JOIN categories c
        ON p.category_id = c.category_id
    """

    category_map = pd.read_sql(
        category_map_query,
        engine
    )

    df = df.merge(
        category_map,
        on="product_id",
        how="left"
    )

    df = df[
        df["category_name"] == selected_category
    ]

st.sidebar.subheader("📅 Date Filter")

df["order_date"] = pd.to_datetime(df["order_date"])

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

selected_dates = st.sidebar.date_input(
"Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    df = df[
        (df["order_date"] >= pd.Timestamp(start_date)) &
        (df["order_date"] <= pd.Timestamp(end_date))
    ]

st.subheader("📊 Business Overview")

total_revenue = df["total_revenue"].sum()
total_profit = df["total_profit"].sum()
total_orders = df["order_id"].nunique()
total_quantity = df["quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "📈 Total Profit",
        f"₹{total_profit:,.2f}"
    )

with col3:
    st.metric(
        "🛒 Total Orders",
        total_orders
    )

with col4:
    st.metric(
        "📦 Total Quantity",
        total_quantity
    )

total_cost = df["total_cost"].sum()

average_order_value = total_revenue / total_orders

profit_margin = (total_profit / total_revenue) * 100

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "💳 Average Order Value",
        f"₹{average_order_value:,.2f}"
    )

with col6:
    st.metric(
        "💰 Total Cost",
        f"₹{total_cost:,.2f}"
    )

with col7:
    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )

st.subheader("📈 Revenue & Profit Trend")

trend_option = st.selectbox(
    "Select Trend",
    ["Daily", "Monthly", "Yearly"]
)

if trend_option == "Daily":

    growth_data = (
        df.groupby(df["order_date"].dt.date)["total_revenue"]
        .sum()
        .sort_index()
    )

elif trend_option == "Monthly":

    growth_data = (
        df.groupby(df["order_date"].dt.to_period("M"))["total_revenue"]
        .sum()
        .sort_index()
    )

else:

    growth_data = (
        df.groupby(df["order_date"].dt.year)["total_revenue"]
        .sum()
        .sort_index()
    )

if len(growth_data) >= 2:

    current_revenue = growth_data.iloc[-1]
    previous_revenue = growth_data.iloc[-2]

    if previous_revenue != 0:
        revenue_growth = (
            (current_revenue - previous_revenue)
            / previous_revenue
        ) * 100
    else:
        revenue_growth = 0

else:
    revenue_growth = 0

with col8:
    st.metric(
        "📈 Revenue Growth",
        f"{revenue_growth:.2f}%"
    )

df["order_date"] = pd.to_datetime(df["order_date"])

if trend_option == "Daily":

    trend_data = (
        df.groupby(df["order_date"].dt.date)
        .agg(
            Revenue=("total_revenue", "sum"),
            Profit=("total_profit", "sum")
        )
        .reset_index()
    )

    trend_data["order_date"] = trend_data["order_date"].astype(str)


elif trend_option == "Monthly":

    trend_data = (
        df.groupby(df["order_date"].dt.to_period("M"))
        .agg(
            Revenue=("total_revenue", "sum"),
            Profit=("total_profit", "sum")
        )
        .reset_index()
    )

    trend_data["order_date"] = trend_data["order_date"].astype(str)


else:

    trend_data = (
        df.groupby(df["order_date"].dt.year)
        .agg(
            Revenue=("total_revenue", "sum"),
            Profit=("total_profit", "sum")
        )
        .reset_index()
    )

    trend_data["order_date"] = trend_data["order_date"].astype(str)


st.line_chart(
    trend_data.set_index("order_date")[["Revenue", "Profit"]]
)

st.subheader("🏷️ Category Performance")

category_map_query = """
SELECT
    p.product_id,
    c.category_name AS Category
FROM products p
JOIN categories c
    ON p.category_id = c.category_id
"""

category_map = pd.read_sql(
    category_map_query,
    engine
)

category_chart_data = df.merge(
    category_map,
    on="product_id",
    how="left"
)

category_data = (
    category_chart_data
    .groupby("Category")
    .agg(
        Revenue=("total_revenue", "sum"),
        Profit=("total_profit", "sum")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    st.write("💰 Revenue by Category")

    st.bar_chart(
        category_data.set_index("Category")["Revenue"]
    )

with col2:
    st.write("📈 Profit by Category")

    st.bar_chart(
        category_data.set_index("Category")["Profit"]
    )

st.subheader("🌍 Regional Performance")

region_map_query = """
SELECT
    region_id,
    region_name AS Region
FROM regions
"""

region_map = pd.read_sql(
    region_map_query,
    engine
)

region_chart_data = df.merge(
    region_map,
    on="region_id",
    how="left"
)

region_data = (
    region_chart_data
    .groupby("Region")
    .agg(
        Revenue=("total_revenue", "sum"),
        Profit=("total_profit", "sum")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    st.write("💰 Revenue by Region")

    st.bar_chart(
        region_data.set_index("Region")["Revenue"]
    )

with col2:
    st.write("📈 Profit by Region")

    st.bar_chart(
        region_data.set_index("Region")["Profit"]
    )

st.subheader("🏆 Top 10 Products")

product_map_query = """
SELECT
    product_id,
    product_name AS Product
FROM products
"""

product_map = pd.read_sql(
    product_map_query,
    engine
)

product_chart_data = df.merge(
    product_map,
    on="product_id",
    how="left"
)

product_data = (
    product_chart_data
    .groupby("Product")
    .agg(
        Revenue=("total_revenue", "sum"),
        Profit=("total_profit", "sum"),
        Quantity=("quantity", "sum")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

col1, col2 = st.columns(2)

with col1:
    st.write("💰 Revenue by Product")

    st.bar_chart(
        product_data.set_index("Product")["Revenue"]
    )

with col2:
    st.write("📋 Product Details")

    st.dataframe(
        product_data,
        use_container_width=True,
        hide_index=True
    )

st.subheader("📊 Category Revenue Contribution")

category_contribution = category_data.copy()

total_category_revenue = category_contribution["Revenue"].sum()

category_contribution["Contribution %"] = (
    category_contribution["Revenue"]
    / total_category_revenue
) * 100

category_contribution["Contribution %"] = (
    category_contribution["Contribution %"].round(2)
)

st.dataframe(
    category_contribution,
    use_container_width=True,
    hide_index=True
)

st.subheader("💹 Product Profitability Analysis")

profitability_data = product_chart_data.copy()

profitability_data = (
    profitability_data
    .groupby("Product")
    .agg(
        Revenue=("total_revenue", "sum"),
        Profit=("total_profit", "sum"),
        Cost=("total_cost", "sum")
    )
    .reset_index()
)

profitability_data["Profit Margin %"] = (
    profitability_data["Profit"]
    / profitability_data["Revenue"]
) * 100

profitability_data["Profit Margin %"] = (
    profitability_data["Profit Margin %"].round(2)
)

profitability_data = profitability_data.sort_values(
    "Profit Margin %",
    ascending=False
)

col1, col2 = st.columns(2)

with col1:
    st.write("📈 Profit by Product")

    st.bar_chart(
        profitability_data.set_index("Product")["Profit"]
    )

with col2:
    st.write("📊 Profit Margin by Product")

    st.bar_chart(
        profitability_data.set_index("Product")["Profit Margin %"]
    )

st.dataframe(
    profitability_data,
    use_container_width=True,
    hide_index=True
)

st.subheader("⚠️ Bottom 5 Products")

bottom_products = (
    product_chart_data
    .groupby("Product")
    .agg(
        Revenue=("total_revenue", "sum"),
        Profit=("total_profit", "sum"),
        Quantity=("quantity", "sum")
    )
    .reset_index()
    .sort_values("Revenue", ascending=True)
    .head(5)
)

st.dataframe(
    bottom_products,
    use_container_width=True,
    hide_index=True
)

st.subheader("🌍 Regional Revenue Contribution")

region_contribution = region_data.copy()

total_region_revenue = region_contribution["Revenue"].sum()

region_contribution["Contribution %"] = (
    region_contribution["Revenue"]
    / total_region_revenue
) * 100

region_contribution["Contribution %"] = (
    region_contribution["Contribution %"].round(2)
)

st.dataframe(
    region_contribution,
    use_container_width=True,
    hide_index=True
)