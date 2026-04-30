import os
import time

import curl_cffi.requests as requests
from dotenv import load_dotenv
from prefect import get_run_logger

load_dotenv()

BASE_URL = os.getenv("DPWH_BASE_URL")
LIMIT = 5000
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
    logger = get_run_logger()
    response = requests.get(
        BASE_URL,
        params={"page": page, "limit": LIMIT},
        headers=HEADERS,
        impersonate=profile,
        timeout=30,
    )
    if response.status_code in (429, 403) and "1015" in response.text:
        logger.info("  Rate limited. Waiting 10 minutes...")
        time.sleep(600)
        raise Exception("Rate limited")
    response.raise_for_status()
    return response.json()


def fetch_with_retry(page: int) -> list[dict] | None:
    logger = get_run_logger()
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
            logger.warning(f"  Page {page} failed with {profile}: {e}")
            time.sleep(5)
    return None


def get_total_pages() -> int:
    logger = get_run_logger()
    logger.info("Fetching page 1 to get total count...")

    for profile in TLS_PROFILES:
        try:
            data = fetch_page(1, profile)
            pagination = data["data"]["pagination"]
            total_count = pagination["totalCount"]
            total_pages = -(-total_count // LIMIT)
            logger.info(f"Total projects : {total_count:,}")
            logger.info(f"Total pages    : {total_pages} (at {LIMIT} per page)")
            return total_pages
        except Exception as e:
            logger.warning(f"  Page 1 failed with {profile}: {e}")
            time.sleep(5)

    raise Exception("All TLS profiles failed on page 1")


def fetch_dpwh_data() -> list[dict]:
    logger = get_run_logger()
    total_pages = get_total_pages()
    all_records = []
    failed_pages = []

    for page in range(1, total_pages + 1):
        records = fetch_with_retry(page)
        if records:
            all_records.extend(records)
            logger.info(
                f"[{page}/{total_pages}] fetched {len(records)} — total: {len(all_records):,}"
            )
        else:
            failed_pages.append(page)
            logger.warning(f"[{page}/{total_pages}] permanently failed, skipping")

        time.sleep(DELAY_SECONDS)

    if failed_pages:
        logger.warning(f"\nFailed pages: {failed_pages}")
        with open("failed_pages.txt", "w") as f:
            f.write("\n".join(map(str, failed_pages)))

    return all_records
