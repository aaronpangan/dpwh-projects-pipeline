import io
import os

import boto3
import duckdb
import pandas as pd
import pyarrow.parquet as pq
from dotenv import load_dotenv
from prefect import get_run_logger

load_dotenv()

S3_KEY = "raw/dpwh_projects_raw.parquet"


def upload_to_s3(records: list[dict]) -> str:
    logger = get_run_logger()
    bucket_name = os.getenv("PROJECT_BUCKET_NAME")
    region_name = os.getenv("REGION_NAME")
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    df = pd.DataFrame(records)
    con = duckdb.connect()
    con.execute("CREATE TABLE dpwh AS SELECT * FROM df")
    arrow_table = con.execute("SELECT * FROM dpwh").to_arrow_table()
    con.close()

    buffer = io.BytesIO()
    pq.write_table(arrow_table, buffer)
    buffer.seek(0)

    s3_client = boto3.client(
        "s3",
        region_name=region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )

    s3_client.upload_fileobj(buffer, bucket_name, S3_KEY)
    s3_path = f"s3://{bucket_name}/{S3_KEY}"
    logger.info(f"Uploaded to {s3_path}")
    return s3_path
