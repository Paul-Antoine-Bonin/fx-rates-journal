# fx-rates-journal

Daily journal of **ECB euro reference rates** for 29 currencies, stored as plain CSV
(`data/EUR<CCY>.csv`, columns `date,rate`) and kept up to date by small, reviewable pull requests.

Each sync either appends the newest fixings or, when there is nothing new (weekends, holidays),
backfills one more year of history back to 2000, so the dataset keeps getting deeper.

## Latest snapshot

<!-- table:start -->
| Pair | Last fixing | Rate | 1d | 20d | 60d vol (ann.) | Rows |
|---|---|---:|---:|---:|---:|---:|
| [EUR/NOK](data/EURNOK.csv) | 2026-10-07 | 10.712 | -0.61% | +0.14% | 4.86% | 196 |
<!-- table:end -->

## Usage

```bash
python3 scripts/sync.py USD          # sync a single pair
python3 scripts/daily.py             # daily job: one PR per pair synced (needs gh CLI)
python3 scripts/daily.py --dry-run   # preview without touching GitHub
```

Load a series:

```python
import pandas as pd
eurusd = pd.read_csv("data/EURUSD.csv", parse_dates=["date"], index_col="date")["rate"]
```

## Source

European Central Bank reference rates via [frankfurter.app](https://www.frankfurter.app/).
Rates are published around 16:00 CET on TARGET business days.

## License

Code: MIT. Data: ECB, see their terms of reuse.

## Maintainers

@Paul-Antoine-Bonin · @ASRIDK
