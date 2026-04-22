import os
from dotenv import load_dotenv

load_dotenv()

import requests
import pandas as pd
import psycopg2
import time
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
    time.sleep(1)

if len(all_contracts) ==0:
    print("No records collected. Exiting.")
    exit()
df = pd.DataFrame(all_contracts)
df= df[["noticeId", "title", "solicitationNumber", "fullParentPathName", "postedDate", "type", "responseDeadLine"]]
df.to_csv("contracts.csv", index = False)
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT")
)
cursor = conn.cursor()
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
print(f"Succesfully loaded {len(all_contracts)} records")
cursor.close()
conn.close()