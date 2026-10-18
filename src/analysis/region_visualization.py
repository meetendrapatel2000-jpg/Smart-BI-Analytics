import pandas as pd
import plotly.express as px

from database import engine


query = """
SELECT
    r.region_name,
    SUM(o.total_revenue) AS revenue,
    SUM(o.total_profit) AS profit
FROM orders o
JOIN regions r
    ON o.region_id = r.region_id
GROUP BY r.region_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)


fig = px.bar(
    df,
    x="region_name",
    y=["revenue", "profit"],
    barmode="group",
    title="Regional Revenue & Profit"
)

fig.update_layout(
    xaxis_title="Region",
    yaxis_title="Amount",
    template="plotly_white"
)

fig.show()