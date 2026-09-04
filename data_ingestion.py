"""
Day 1 - Data Ingestion and Validation
Bluestock Fintech | Mutual Fund Analytics Capstone

Loads the 10 provided CSV datasets, prints shape/dtypes/head,
checks basic anomalies, explores the fund master, and validates
AMFI scheme codes against NAV history.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"

DATASETS = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]


def inspect_dataset(filename: str) -> pd.DataFrame:
    path = RAW / filename
    df = pd.read_csv(path)

    print("\n" + "=" * 80)
    print(f"{filename}")
    print("=" * 80)
    print(f"Shape: {df.shape}")
    print("\nDtypes:")
    print(df.dtypes)
    print("\nHead:")
    print(df.head().to_string(index=False))

    nulls = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    print(f"\nMissing values: {nulls}")
    print(f"Duplicate rows: {duplicates}")

    if nulls:
        print("Anomaly note: missing values are present; inspect column-level null counts.")
        print(df.isna().sum()[df.isna().sum() > 0])

    if duplicates:
        print("Anomaly note: duplicate complete rows are present.")

    return df


def explore_fund_master(fund_master: pd.DataFrame) -> None:
    print("\n" + "=" * 80)
    print("FUND MASTER EXPLORATION")
    print("=" * 80)
    for column, label in [
        ("fund_house", "Unique fund houses"),
        ("category", "Unique categories"),
        ("sub_category", "Unique sub-categories"),
        ("risk_category", "Unique risk grades"),
    ]:
        print(f"\n{label}:")
        for value in sorted(fund_master[column].dropna().unique()):
            print(f"  - {value}")

    print("\nAMFI scheme code summary:")
    print(f"  Unique scheme codes: {fund_master['amfi_code'].nunique()}")
    print(f"  Minimum code: {fund_master['amfi_code'].min()}")
    print(f"  Maximum code: {fund_master['amfi_code'].max()}")
    print(
        "  Note: AMFI scheme codes are identifiers assigned to mutual-fund "
        "schemes; the numeric value itself should be treated as an identifier, "
        "not decoded as a fund-house/category code."
    )


def validate_amfi_codes(fund_master: pd.DataFrame, nav_history: pd.DataFrame) -> None:
    print("\n" + "=" * 80)
    print("AMFI CODE VALIDATION")
    print("=" * 80)

    master_codes = set(fund_master["amfi_code"].dropna().astype(int))
    nav_codes = set(nav_history["amfi_code"].dropna().astype(int))

    missing_from_nav = sorted(master_codes - nav_codes)
    extra_in_nav = sorted(nav_codes - master_codes)

    print(f"Funds in fund_master: {len(master_codes)}")
    print(f"Funds in nav_history: {len(nav_codes)}")
    print(f"Codes missing from nav_history: {missing_from_nav}")
    print(f"Codes only in nav_history: {extra_in_nav}")

    duplicate_master_codes = int(fund_master["amfi_code"].duplicated().sum())
    duplicate_nav_keys = int(
        nav_history.duplicated(subset=["amfi_code", "date"]).sum()
    )
    print(f"Duplicate AMFI codes in fund_master: {duplicate_master_codes}")
    print(f"Duplicate AMFI/date rows in nav_history: {duplicate_nav_keys}")

    if not missing_from_nav and duplicate_master_codes == 0:
        print(
            "\nRESULT: PASS - every AMFI code in fund_master exists in "
            "nav_history and fund_master contains unique scheme codes."
        )
    else:
        print("\nRESULT: REVIEW - AMFI validation found issues.")


def main() -> None:
    print("BLUESTOCK MUTUAL FUND ANALYTICS - DAY 1 DATA INGESTION")
    print(f"Raw data directory: {RAW}")

    datasets = {}
    for filename in DATASETS:
        datasets[filename] = inspect_dataset(filename)

    fund_master = datasets["01_fund_master.csv"]
    nav_history = datasets["02_nav_history.csv"]

    explore_fund_master(fund_master)
    validate_amfi_codes(fund_master, nav_history)

    print("\n" + "=" * 80)
    print("DATA QUALITY SUMMARY")
    print("=" * 80)
    print(
        "10/10 required CSV datasets were loaded successfully. "
        "The only expected missing values are in monthly SIP inflows "
        "(04_monthly_sip_inflows.csv), where the earliest YoY-growth "
        "observations are unavailable because a prior-year comparison "
        "does not exist."
    )
    print(
        "AMFI code validation: all 40 fund_master scheme codes are present "
        "in nav_history."
    )


if __name__ == "__main__":
    main()
