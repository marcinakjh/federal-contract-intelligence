import os
from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT")
)

df = pd.read_sql("SELECT * FROM contracts", conn)
df.columns = df.columns.str.lower()
df.to_csv("contracts.csv", index=False)

conn.close()

print(f"Exported {len(df)} records to contracts.csv")