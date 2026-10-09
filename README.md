# fx-rates-journal

Daily journal of **ECB euro reference rates** for 29 currencies, stored as plain CSV
(`data/EUR<CCY>.csv`, columns `date,rate`) and kept up to date by small, reviewable pull requests.

Each sync either appends the newest fixings or, when there is nothing new (weekends, holidays),
backfills one more year of history back to 2000, so the dataset keeps getting deeper.

## Latest snapshot

<!-- table:start -->
| Pair | Last fixing | Rate | 1d | 20d | 60d vol (ann.) | Rows |
|---|---|---:|---:|---:|---:|---:|
| [EUR/AUD](data/EURAUD.csv) | 2026-10-07 | 1.6079 | -0.38% | -0.30% | 4.65% | 196 |
| [EUR/BRL](data/EURBRL.csv) | 2026-10-07 | 5.5953 | -0.07% | -5.64% | 12.48% | 196 |
| [EUR/CAD](data/EURCAD.csv) | 2026-10-08 | 1.5953 | +0.14% | -0.60% | 4.06% | 197 |
| [EUR/CHF](data/EURCHF.csv) | 2026-10-07 | 0.9309 | -0.53% | -1.01% | 5.17% | 196 |
| [EUR/CNY](data/EURCNY.csv) | 2026-10-07 | 7.4937 | -0.82% | -4.12% | 4.49% | 196 |
| [EUR/CZK](data/EURCZK.csv) | 2026-10-07 | 24.427 | +0.09% | +0.74% | 1.73% | 451 |
| [EUR/DKK](data/EURDKK.csv) | 2026-10-07 | 7.4745 | -0.00% | -0.00% | 0.08% | 196 |
| [EUR/ILS](data/EURILS.csv) | 2026-10-07 | 3.429 | -0.17% | -2.53% | 7.83% | 196 |
| [EUR/INR](data/EURINR.csv) | 2026-10-07 | 108.1165 | -0.50% | -2.44% | 5.23% | 196 |
| [EUR/KRW](data/EURKRW.csv) | 2026-10-07 | 1496.25 | -0.82% | -3.90% | 8.58% | 196 |
| [EUR/MXN](data/EURMXN.csv) | 2026-10-07 | 20.2236 | +0.01% | +2.68% | 6.01% | 196 |
| [EUR/NOK](data/EURNOK.csv) | 2026-10-07 | 10.712 | -0.61% | +0.14% | 4.86% | 196 |
| [EUR/NZD](data/EURNZD.csv) | 2026-10-08 | 2.0014 | +0.19% | +0.37% | 4.90% | 197 |
| [EUR/PHP](data/EURPHP.csv) | 2026-10-07 | 70.203 | -0.71% | -3.59% | 5.44% | 196 |
| [EUR/PLN](data/EURPLN.csv) | 2026-10-07 | 4.3825 | +0.40% | +1.56% | 3.53% | 196 |
| [EUR/SEK](data/EURSEK.csv) | 2026-10-07 | 11.224 | -0.16% | +0.67% | 3.63% | 196 |
| [EUR/THB](data/EURTHB.csv) | 2026-10-07 | 37.661 | -0.46% | -1.68% | 4.43% | 196 |
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
