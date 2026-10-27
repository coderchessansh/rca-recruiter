#!/usr/bin/env python3
"""Build a candidate list from a public Scratch studio roster.

Read-only: this script does not invite, follow, message, or comment on anyone.
"""
import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

STUDIO_ID = os.environ.get("SCRATCH_STUDIO_ID", "35469041")
API_BASE = "https://api.scratch.mit.edu"
PAGE_SIZE = 40
OUTPUT_FILE = "rca_candidates.txt"
JSON_OUTPUT_FILE = "candidates.json"


def fetch_json(url):
    request = Request(url, headers={"User-Agent": "RCA-Candidate-List/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Scratch API returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach Scratch API: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("Scratch API returned invalid JSON") from exc


def get_host(studio):
    for key in ("host", "owner"):
        value = studio.get(key)
        if isinstance(value, dict) and value.get("username"):
            return value["username"]
        if isinstance(value, str):
            return value
    return None


def get_roster(endpoint):
    usernames = []
    offset = 0
    while True:
        url = f"{API_BASE}/studios/{STUDIO_ID}/{endpoint}/?limit={PAGE_SIZE}&offset={offset}"
        data = fetch_json(url)
        if not isinstance(data, list) or not data:
            break
        for item in data:
            if not isinstance(item, dict):
                continue
            username = item.get("username")
            if not username and isinstance(item.get("user"), dict):
                username = item["user"].get("username")
            if isinstance(username, str) and username.strip():
                usernames.append(username.strip())
        if len(data) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.25)
    return usernames


def main():
    try:
        studio = fetch_json(f"{API_BASE}/studios/{STUDIO_ID}")
        if not isinstance(studio, dict):
            raise RuntimeError("Unexpected studio details response")
        host = get_host(studio)
        managers = get_roster("managers")
        curators = get_roster("curators")
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("Scratch's public API may have changed or be temporarily unavailable.", file=sys.stderr)
        return 1

    candidates = []
    seen = set()
    host_key = host.casefold() if host else None
    for username in managers + curators:
        key = username.casefold()
        if key in seen or (host_key and key == host_key):
            continue
        seen.add(key)
        candidates.append(username)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        output.write(f"RCA candidate list from Scratch studio {STUDIO_ID}\n")
        output.write("Source: public managers and curators roster\n")
        output.write("Host excluded when identifiable. No invitations were sent.\n\n")
        output.writelines(username + "\n" for username in candidates)

    with open(JSON_OUTPUT_FILE, "w", encoding="utf-8") as output:
        json.dump({
            "studio_id": STUDIO_ID,
            "host": host,
            "managers_count": len(managers),
            "curators_count": len(curators),
            "candidates": [{"username": username} for username in candidates],
        }, output, ensure_ascii=False, indent=2)
        output.write("\n")

    print(f"Host: {host or 'not identified by API'}")
    print(f"Managers: {len(managers)} | Curators: {len(curators)}")
    print(f"Unique candidates: {len(candidates)}")
    print(f"Created {OUTPUT_FILE}")
    if not host:
        print("Note: host was not identified, so host exclusion could not be confirmed.")
    print("Review the list and invite people manually and respectfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
