import pandas as pd

from database import engine


query = """
SELECT
    p.product_name,
    c.category_name,
    SUM(o.quantity) AS quantity,
    SUM(o.total_revenue) AS revenue,
    SUM(o.total_cost) AS cost,
    SUM(o.total_profit) AS profit
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN categories c
    ON p.category_id = c.category_id
GROUP BY p.product_name, c.category_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)

print("\nProduct Performance")
print("-" * 50)
print(df)