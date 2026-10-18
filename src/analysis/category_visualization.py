import pandas as pd
import plotly.express as px

from database import engine


query = """
SELECT
    c.category_name,
    SUM(o.total_revenue) AS revenue,
    SUM(o.total_profit) AS profit
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN categories c
    ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)


fig = px.bar(
    df,
    x="category_name",
    y="revenue",
    title="Revenue by Category",
    text_auto=".2s"
)

fig.update_layout(
    xaxis_title="Category",
    yaxis_title="Revenue",
    template="plotly_white"
)

fig.show()