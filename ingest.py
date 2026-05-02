# ============================================================
# SAM.gov Data Pipeline
# ============================================================
# Pulls federal contract opportunity records from the SAM.gov
# REST API, paginates through results with rate limiting, writes
# the raw data to a local CSV, and loads it into a PostgreSQL
# database for downstream analysis and reporting.
#
# Requires: SAM.gov API key and PostgreSQL credentials in .env
#           (see .env.example)
# Output: contracts.csv (project root) and 'contracts' table in PostgreSQL
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

import requests
import pandas as pd
import psycopg2
import time

# ------------------------------------------------------------
# Configuration: API credentials, endpoint, and request parameters
# ------------------------------------------------------------
# Loads the SAM.gov API key from .env and configures the request
# to pull all federal contract opportunities posted in 2024,
# in batches of 1,000 records per API call.

API_KEY = os.environ.get("SAM_API_KEY")
url = "https://api.sam.gov/opportunities/v2/search"
all_contracts = []
offset = 0
params = {
    "api_key": API_KEY,
    "limit": 1000,
    "postedFrom": "01/01/2024",
    "postedTo": "12/31/2024"
}

# ------------------------------------------------------------
# Pagination Loop: Pull records in batches with rate limiting
# ------------------------------------------------------------
# Iterates through SAM.gov API responses, accumulating records
# until either the target volume is reached or the API returns
# no more results. Includes a 1-second delay between requests
# to respect SAM.gov rate limits.

while len(all_contracts) < 2000:
    params["offset"] = offset
    response = requests.get(url, params=params)
    if "opportunitiesData" not in response.json():
        print("Rate limit hit or error:", response.json())
        break
    records = response.json()["opportunitiesData"]
    if len(records) == 0:
        print(f"No more records available. Total collected: {len(all_contracts)}")
        break
    all_contracts = all_contracts + records
    offset = offset + 1000
    time.sleep(1) # Respect SAM.gov rate limits between paginated requests

if len(all_contracts) ==0:
    print("No records collected. Exiting.")
    exit()

# ------------------------------------------------------------
# Transform: Convert API records to a structured DataFrame
# ------------------------------------------------------------
# Selects the columns needed for downstream analysis and writes
# the cleaned data to a local CSV for inspection and backup.

df = pd.DataFrame(all_contracts)
df= df[["noticeId", "title", "solicitationNumber", "fullParentPathName", "postedDate", "type", "responseDeadLine"]]
df.to_csv("contracts.csv", index = False)

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
cursor = conn.cursor()

# ------------------------------------------------------------
# Schema and Load: Create the contracts table and insert records
# ------------------------------------------------------------
# Creates the contracts table if it does not already exist, then
# bulk-inserts the cleaned records using executemany for efficiency.

cursor.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        noticeId TEXT,
        title TEXT,
        solicitationNumber TEXT,
        fullParentPathName TEXT,
        postedDate TEXT,
        type TEXT,
        responseDeadLine TEXT
    );
""")
conn.commit()
data = [tuple(row) for row in df.itertuples(index=False)]
cursor.executemany("INSERT INTO contracts (noticeId, title, solicitationNumber, fullParentPathName, postedDate, type, responseDeadLine) VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
conn.commit()
print(f"Successfully loaded {len(all_contracts)} records")
cursor.close()
conn.close()
