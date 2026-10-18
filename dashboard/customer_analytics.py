import sys
from pathlib import Path

import streamlit as st
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.database import engine

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Analytics")
st.write("Analyze customer orders, revenue and profit.")

query = """
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_revenue), 0) AS total_revenue,
    COALESCE(SUM(o.total_profit), 0) AS total_profit
FROM custormers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC
"""

df = pd.read_sql(query, engine)

if df.empty:
    st.warning("No customer data found.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Customers", df["customer_name"].nunique())

    with col2:
        st.metric("Total Revenue", f"₹{df['total_revenue'].sum():,.2f}")

    with col3:
        st.metric("Total Profit", f"₹{df['total_profit'].sum():,.2f}")

    st.subheader("Customer Performance")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Revenue by Customer")

    chart_df = df.set_index("customer_name")
    st.bar_chart(chart_df["total_revenue"])

    csv_data = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Customer Report",
        data=csv_data,
        file_name="customer_analytics.csv",
        mime="text/csv"
    )