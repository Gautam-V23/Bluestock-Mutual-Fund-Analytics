# Day 1 — Data Quality Summary

All 10 required CSV datasets were loaded successfully.

| Dataset | Rows | Columns |
|---|---:|---:|
| 01_fund_master.csv | 40 | 15 |
| 02_nav_history.csv | 46,000 | 3 |
| 03_aum_by_fund_house.csv | 90 | 5 |
| 04_monthly_sip_inflows.csv | 48 | 6 |
| 05_category_inflows.csv | 144 | 3 |
| 06_industry_folio_count.csv | 21 | 6 |
| 07_scheme_performance.csv | 40 | 19 |
| 08_investor_transactions.csv | 32,778 | 13 |
| 09_portfolio_holdings.csv | 322 | 8 |
| 10_benchmark_indices.csv | 8,050 | 3 |

## Anomaly

`04_monthly_sip_inflows.csv` has missing `yoy_growth_pct` values for the earliest observations. These are expected because YoY growth requires a prior-year comparison.

## Fund master

- 10 unique fund houses
- 2 categories
- 12 sub-categories
- 5 risk grades
- 40 unique AMFI scheme codes

AMFI scheme codes are scheme identifiers; the numeric code should be treated as an identifier rather than a code that directly encodes fund-house or category information.

## AMFI validation

All 40 AMFI scheme codes in `01_fund_master.csv` exist in `02_nav_history.csv`.

**Result: PASS.**
