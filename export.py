# ============================================================
# PostgreSQL to CSV Export
# ============================================================
# Reads the current contents of the 'contracts' table in PostgreSQL
# and writes a snapshot to contracts.csv with lowercased column
# names for downstream use in Tableau.
#
# This script is run after one or more sessions of ingest.py
# have populated the database. It produces a clean, dashboard-ready
# CSV reflecting the latest state of the contracts table.
#
# Requires: PostgreSQL credentials in .env (see .env.example)
# Input: 'contracts' table in PostgreSQL
# Output: contracts.csv (overwrites any prior version in project root)
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import psycopg2

# ------------------------------------------------------------
# Database Connection: Connect to PostgreSQL using env credentials
# ------------------------------------------------------------

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT")
)

# ------------------------------------------------------------
# Read and Export: Pull the contracts table and write to CSV
# ------------------------------------------------------------
# Lowercases column names so they are consistent with Tableau and
# SQL conventions, then overwrites contracts.csv with the snapshot.

df = pd.read_sql("SELECT * FROM contracts", conn)
df.columns = df.columns.str.lower()
df.to_csv("contracts.csv", index=False)

conn.close()

print(f"Exported {len(df)} records to contracts.csv")
