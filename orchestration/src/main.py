import time

import curl_cffi.requests as requests
import duckdb
import pandas as pd

BASE_URL = "https://api.transparency.dpwh.gov.ph/projects"
LIMIT = 5000
OUTPUT_PATH = "dpwh_projects_raw.parquet"
DELAY_SECONDS = 2

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


def save_to_parquet(records: list[dict]) -> None:

    df = pd.DataFrame(records)
    con = duckdb.connect()
    con.execute("CREATE TABLE dpwh AS SELECT * FROM df")
    con.execute(f"COPY dpwh TO '{OUTPUT_PATH}' (FORMAT PARQUET)")
    count = con.execute("SELECT COUNT(*) FROM dpwh").fetchone()[0]
    con.close()
    print(f"Saved {count:,} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    print("Starting DPWH full extraction...\n")
    records = fetch_all()
    print(f"\nExtraction complete. Total records: {len(records):,}")
    print("Saving to parquet...")
    save_to_parquet(records)
    print("Done.")
