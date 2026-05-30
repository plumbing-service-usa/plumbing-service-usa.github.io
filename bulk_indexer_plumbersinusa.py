"""
Bulk Google Indexing API submitter for plumbersinusa.com
Fetches all URLs from sitemap, submits to Google Indexing API.

Requirements:
    pip install google-auth google-auth-httplib2 requests

Setup:
    1. Place your Google service account JSON key file in this directory
    2. Set SERVICE_ACCOUNT_FILE below to your JSON filename
    3. Run: python bulk_indexer_plumbersinusa.py
"""

import json
import time
import os
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# ─── CONFIG ────────────────────────────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = "service_account.json"   # <-- change to your JSON filename
SITEMAP_URL          = "https://plumbersinusa.com/sitemap.xml"
LOG_FILE             = "indexing_log_plumbersinusa.json"
DAILY_QUOTA          = 200          # Google Indexing API daily limit
DELAY_BETWEEN_CALLS  = 0.5         # seconds between API calls (be polite)
# ────────────────────────────────────────────────────────────────────────────────

SCOPES = ["https://www.googleapis.com/auth/indexing"]
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def get_credentials():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"\n[ERROR] Service account file '{SERVICE_ACCOUNT_FILE}' not found.")
        print("  1. Go to Google Cloud Console → IAM & Admin → Service Accounts")
        print("  2. Create/select a service account with Indexing API access")
        print("  3. Download the JSON key and place it in this folder")
        print(f"  4. Rename it to: {SERVICE_ACCOUNT_FILE}")
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return creds


def get_access_token(creds):
    creds.refresh(Request())
    return creds.token


def fetch_sitemap_urls(sitemap_url):
    """Recursively fetch all URLs from sitemap or sitemap index."""
    print(f"  Fetching: {sitemap_url}")
    try:
        resp = requests.get(sitemap_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [WARN] Could not fetch {sitemap_url}: {e}")
        return []

    root = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # Sitemap index (contains <sitemap> tags)
    sub_sitemaps = root.findall("sm:sitemap/sm:loc", ns)
    if sub_sitemaps:
        urls = []
        for loc in sub_sitemaps:
            urls.extend(fetch_sitemap_urls(loc.text.strip()))
        return urls

    # Regular sitemap (contains <url> tags)
    return [loc.text.strip() for loc in root.findall("sm:url/sm:loc", ns)]


def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {"submitted": [], "errors": [], "last_run": None}


def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def submit_url(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"url": url, "type": "URL_UPDATED"}
    resp = requests.post(INDEXING_ENDPOINT, headers=headers, json=payload, timeout=30)
    return resp.status_code, resp.json()


def main():
    print("=" * 60)
    print("  Google Bulk Indexer — plumbersinusa.com")
    print("=" * 60)

    creds = get_credentials()
    log = load_log()
    already_submitted = set(log["submitted"])

    print(f"\n[1/3] Fetching sitemap URLs from {SITEMAP_URL} ...")
    all_urls = fetch_sitemap_urls(SITEMAP_URL)
    all_urls = list(dict.fromkeys(all_urls))   # deduplicate, preserve order
    print(f"      Found {len(all_urls)} total URLs")

    pending = [u for u in all_urls if u not in already_submitted]
    print(f"      {len(already_submitted)} already submitted, {len(pending)} remaining")

    if not pending:
        print("\n[DONE] All URLs already submitted!")
        return

    to_submit = pending[:DAILY_QUOTA]
    print(f"\n[2/3] Submitting up to {DAILY_QUOTA} URLs today ...")
    print(f"      Will submit: {len(to_submit)} URLs\n")

    token = get_access_token(creds)
    success, failed = 0, 0

    for i, url in enumerate(to_submit, 1):
        # Refresh token every 50 requests (tokens expire after 1 hour)
        if i % 50 == 0:
            token = get_access_token(creds)

        status_code, resp_body = submit_url(url, token)

        if status_code == 200:
            success += 1
            log["submitted"].append(url)
            print(f"  [{i:>4}/{len(to_submit)}] OK     {url}")
        else:
            failed += 1
            error_msg = resp_body.get("error", {}).get("message", str(resp_body))
            log["errors"].append({"url": url, "error": error_msg, "time": str(datetime.now())})
            print(f"  [{i:>4}/{len(to_submit)}] FAIL   {url}")
            print(f"           Error: {error_msg}")
            # Stop immediately if daily quota is exhausted
            if "Quota exceeded" in error_msg:
                print("\n  [!] Daily quota exhausted — stopping. Run again tomorrow.")
                save_log(log)
                break

        save_log(log)
        time.sleep(DELAY_BETWEEN_CALLS)

    log["last_run"] = str(datetime.now())
    save_log(log)

    remaining_after_today = len(pending) - len(to_submit)
    print("\n" + "=" * 60)
    print(f"[3/3] Summary")
    print(f"      Success  : {success}")
    print(f"      Failed   : {failed}")
    print(f"      Remaining: {remaining_after_today} (run again tomorrow)")
    print(f"      Log saved: {LOG_FILE}")
    print("=" * 60)

    if remaining_after_today > 0:
        days_left = (remaining_after_today + DAILY_QUOTA - 1) // DAILY_QUOTA
        print(f"\n  Run this script again each day. ~{days_left} more day(s) to finish.")


if __name__ == "__main__":
    main()
