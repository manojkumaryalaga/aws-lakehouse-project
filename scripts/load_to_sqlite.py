import pandas as pd
import sqlite3
import boto3
import io

BUCKET = "lakehouse-project-manoj"
PROCESSED_KEY = "processed/yellow_tripdata_cleaned.csv"

print("Reading cleaned data from S3...")
s3 = boto3.client("s3")
obj = s3.get_object(Bucket=BUCKET, Key=PROCESSED_KEY)
df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)

print(f"Loading {len(df)} rows into SQLite...")
conn = sqlite3.connect("C:\\projects\\lakehouse\\lakehouse.db")
df.to_sql("raw_taxi_trips", conn, if_exists="replace", index=False)
conn.close()

print("Done! Data loaded into SQLite.")