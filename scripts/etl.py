import boto3
import pandas as pd
import io

BUCKET = "lakehouse-project-manoj"
RAW_KEY = "raw/yellow_tripdata_2021-01.csv"
PROCESSED_KEY = "processed/yellow_tripdata_cleaned.csv"

s3 = boto3.client("s3")

print("Reading data from S3...")
obj = s3.get_object(Bucket=BUCKET, Key=RAW_KEY)
df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)

print(f"Rows before cleaning: {len(df)}")

df = df.dropna()
df = df[df["trip_distance"] > 0]
df = df[df["fare_amount"] > 0]
df = df[df["passenger_count"] > 0]

print(f"Rows after cleaning: {len(df)}")

buffer = io.StringIO()
df.to_csv(buffer, index=False)
s3.put_object(Bucket=BUCKET, Key=PROCESSED_KEY, Body=buffer.getvalue())

print("Cleaned data uploaded to S3 processed/ folder!")