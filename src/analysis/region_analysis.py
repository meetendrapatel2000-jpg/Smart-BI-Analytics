import pandas as pd

from database import engine


query = """
SELECT
    r.region_name,
    SUM(o.total_revenue) AS revenue,
    SUM(o.total_cost) AS cost,
    SUM(o.total_profit) AS profit,
    SUM(o.quantity) AS quantity,
    COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN regions r
    ON o.region_id = r.region_id
GROUP BY r.region_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)

print("\nRegional Performance")
print("-" * 40)
print(df)