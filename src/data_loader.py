import pandas as pd

from database import engine


query = "SELECT * FROM orders"

df = pd.read_sql(query, engine)

print(df)
print("\nShape:", df.shape)