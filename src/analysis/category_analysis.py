import pandas as pd

from database import engine


query = """
SELECT
    c.category_name,
    SUM(o.total_revenue) AS revenue,
    SUM(o.total_cost) AS cost,
    SUM(o.total_profit) AS profit,
    SUM(o.quantity) AS quantity
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN categories c
    ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)

print("\nCategory Performance")
print("-" * 40)
print(df)