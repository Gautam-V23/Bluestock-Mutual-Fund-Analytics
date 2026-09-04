"""
Day 1 - Live NAV Fetcher
Fetches NAV history from mfapi.in and saves raw CSV files.

Required schemes:
125497 HDFC Top 100 Direct
119551 SBI Bluechip
120503 ICICI Bluechip
118632 Nippon Large Cap
119092 Axis Bluechip
120841 Kotak Bluechip
"""

from pathlib import Path
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"

FUNDS = {
    "HDFC_TOP_100": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippom_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841",
}

API_TEMPLATE = "https://api.mfapi.in/mf/{code}"


def fetch_nav(name: str, code: str) -> Path:
    url = API_TEMPLATE.format(code=code)
    print(f"Fetching {name} ({code})...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()

    records = payload.get("data", [])
    if not records:
        raise ValueError(f"No NAV records returned for {name} ({code}).")

    df = pd.DataFrame(records)

    # Keep the raw API fields while adding the scheme code for traceability.
    df.insert(0, "amfi_code", int(code))

    output = RAW / f"{code}_{name}_live.csv"
    df.to_csv(output, index=False)

    print(f"Saved {len(df):,} records -> {output}")
    return output


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    print("MFAPI LIVE NAV FETCH")
    print("-" * 60)

    failures = []
    for name, code in FUNDS.items():
        try:
            fetch_nav(name, code)
        except Exception as exc:
            failures.append((name, code, str(exc)))
            print(f"ERROR: {exc}")

    print("-" * 60)
    if failures:
        print("Completed with failures:")
        for name, code, error in failures:
            print(f"  {name} ({code}): {error}")
        raise SystemExit(1)

    print("All 6 live NAV downloads completed successfully.")


if __name__ == "__main__":
    main()
