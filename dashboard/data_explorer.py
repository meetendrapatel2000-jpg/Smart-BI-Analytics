import sys
from pathlib import Path

import streamlit as st
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.database import engine


st.title("Data Explorer")

query = """
SELECT
    o.*,
    p.product_name,
    c.customer_name
FROM orders o
LEFT JOIN products p
    ON o.product_id = p.product_id
LEFT JOIN custormers c
    ON o.customer_id = c.customer_id
"""

df = pd.read_sql(query, engine)

with engine.connect() as connection:
    print("Connected database:", connection.exec_driver_sql(
        "SELECT DATABASE()"
    ).scalar())

    print("Available tables:", connection.exec_driver_sql(
        "SHOW TABLES"
    ).fetchall())

st.subheader("🔎 Search Records")

search_term = st.text_input(
    "Search by Order ID, Product ID, Customer ID, Product Name or Customer Name"
)

if search_term:
    search_term = search_term.strip()

    search_mask = (
        df["order_id"].astype(str).str.contains(search_term, case=False, na=False) |
        df["product_id"].astype(str).str.contains(search_term, case=False, na=False) |
        df["customer_id"].astype(str).str.contains(search_term, case=False, na=False) |
        df["product_name"].astype(str).str.contains(search_term, case=False, na=False)
    )

    df = df[search_mask]

df["order_date"] = pd.to_datetime(df["order_date"])

st.sidebar.header("Filters")

regions = ["All"] + sorted(df["region_id"].unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

if selected_region != "All":
    df = df[df["region_id"] == selected_region]

st.sidebar.subheader("Date Filter")

min_date = df["order_date"].min()
max_date = df["order_date"].max()

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

st.sidebar.subheader("Search Order")

search_order = st.sidebar.text_input(
    "Enter Order ID"
)

if search_order:
    df = df[
        df["order_id"].astype(str).str.contains(
            search_order,
            case=False,
            na=False
        )
    ]

st.sidebar.subheader("Search Product")

search_product = st.sidebar.text_input(
    "Enter Product ID"
)

if search_product:
    df = df[
        df["product_id"].astype(str).str.contains(
            search_product,
            case=False,
            na=False
        )
    ]

st.sidebar.subheader("Search Customer")

search_customer = st.sidebar.text_input(
    "Enter Customer ID"
)

if search_customer:
    df = df[
        df["customer_id"].astype(str).str.contains(
            search_customer,
            case=False,
            na=False
        )
    ]

st.sidebar.subheader("Category Filter")

category_query = """
SELECT DISTINCT c.category_name
FROM categories c
ORDER BY c.category_name
"""

customer_query = """
SELECT DISTINCT customer_name
FROM custormers
ORDER BY customer_name
"""

customer_df = pd.read_sql(customer_query, engine)

customer_names = ["All Customers"] + customer_df[
    "customer_name"
].dropna().tolist()

selected_customer = st.sidebar.selectbox(
    "Select Customer",
    customer_names
)

if selected_customer != "All Customers":
    df = df[df["customer_name"] == selected_customer]

category_df = pd.read_sql(category_query, engine)

categories = ["All"] + category_df["category_name"].tolist()

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

if selected_category != "All":
    df = df.merge(
        pd.read_sql(
            """
            SELECT p.product_id, c.category_name
            FROM products p
            JOIN categories c
                ON p.category_id = c.category_id
            """,
            engine
        ),
        on="product_id",
        how="left"
    )

    df = df[df["category_name"] == selected_category]

st.sidebar.subheader("Sort Data")

sort_order = st.sidebar.selectbox(
    "Sort by Revenue",
    ["None", "High to Low", "Low to High"]
)

if sort_order == "High to Low":
    df = df.sort_values("total_revenue", ascending=False)

elif sort_order == "Low to High":
    df = df.sort_values("total_revenue", ascending=True)

total_revenue = df["total_revenue"].sum()

st.metric(
    "Total Revenue",
    f"₹{total_revenue:,.2f}"
)

total_profit = df["total_profit"].sum()

st.metric(
    "Total Profit",
    f"₹{total_profit:,.2f}"
)

total_orders = df["order_id"].nunique()

st.metric(
    "Total Orders",
    total_orders
)

total_quantity = df["quantity"].sum()

st.metric(
    "Total Quantity",
    total_quantity
)

st.subheader("Orders Data")

st.write(f"Showing {len(df)} records")

st.dataframe(
    df,
    use_container_width=True
)

csv_data = df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="filtered_orders.csv",
    mime="text/csv"
)

# Download filtered data as Excel
import io

excel_buffer = io.BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Orders Data")

st.download_button(
    label="📊 Download Excel File",
    data=excel_buffer.getvalue(),
    file_name="filtered_orders.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)