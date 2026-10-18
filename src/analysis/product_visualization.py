import pandas as pd
import plotly.express as px

from database import engine


query = """
SELECT
    p.product_name,
    SUM(o.total_revenue) AS revenue,
    SUM(o.total_profit) AS profit
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)


fig = px.bar(
    df,
    x="revenue",
    y="product_name",
    orientation="h",
    title="Top Products by Revenue",
    text_auto=".2s"
)

fig.update_layout(
    xaxis_title="Revenue",
    yaxis_title="Product",
    template="plotly_white"
)

fig.show()