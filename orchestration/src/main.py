import io
import os
import time

import boto3
import curl_cffi.requests as requests
import duckdb
import pandas as pd
import pyarrow.parquet as pq
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.transparency.dpwh.gov.ph/projects"
LIMIT = 5000
S3_KEY = "raw/dpwh_projects_raw.parquet"
DELAY_SECONDS = 3

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.7",
    "origin": "https://transparency.dpwh.gov.ph",
    "referer": "https://transparency.dpwh.gov.ph/",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Brave";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
}

TLS_PROFILES = [
    "chrome120",
    "firefox110",
    "firefox119",
    "safari15_3",
    "safari17_0",
]


def fetch_page(page: int, profile: str = "chrome120") -> dict:
    response = requests.get(
        BASE_URL,
        params={"page": page, "limit": LIMIT},
        headers=HEADERS,
        impersonate=profile,
        timeout=30,
    )
    if response.status_code in (429, 403) and "1015" in response.text:
        print("  Rate limited. Waiting 10 minutes...")
        time.sleep(600)
        raise Exception("Rate limited")
    response.raise_for_status()
    return response.json()


def fetch_with_retry(page: int) -> list[dict] | None:
    for profile in TLS_PROFILES:
        try:
            data = fetch_page(page, profile)
            records = data["data"]["data"]
            for r in records:
                r["province"] = r["location"]["province"]
                r["region"] = r["location"]["region"]
                del r["location"]
            return records
        except Exception as e:
            print(f"  Page {page} failed with {profile}: {e}")
            time.sleep(5)
    return None


def get_total_pages() -> int:
    print("Fetching page 1 to get total count...")
    data = fetch_page(1)
    pagination = data["data"]["pagination"]
    total_count = pagination["totalCount"]
    total_pages = -(-total_count // LIMIT)
    print(f"Total projects : {total_count:,}")
    print(f"Total pages    : {total_pages} (at {LIMIT} per page)")
    return total_pages


def fetch_all() -> list[dict]:
    total_pages = get_total_pages()
    all_records = []
    failed_pages = []

    for page in range(1, total_pages + 1):
        records = fetch_with_retry(page)
        if records:
            all_records.extend(records)
            print(
                f"[{page}/{total_pages}] fetched {len(records)} — total: {len(all_records):,}"
            )
        else:
            failed_pages.append(page)
            print(f"[{page}/{total_pages}] permanently failed, skipping")

        time.sleep(DELAY_SECONDS)

    if failed_pages:
        print(f"\nFailed pages: {failed_pages}")
        with open("failed_pages.txt", "w") as f:
            f.write("\n".join(map(str, failed_pages)))

    return all_records


def upload_to_s3(records: list[dict]) -> str:
    bucket_name = os.getenv("BUCKET_NAME")
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
    print(f"Uploaded to {s3_path}")
    return s3_path


if __name__ == "__main__":
    print("Starting DPWH full extraction...\n")
    records = fetch_all()
    print(f"\nExtraction complete. Total records: {len(records):,}")
    print("Uploading to S3...")
    upload_to_s3(records)
    print("Done.")
