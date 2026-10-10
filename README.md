# fx-rates-journal

Daily journal of **ECB euro reference rates** for 29 currencies, stored as plain CSV
(`data/EUR<CCY>.csv`, columns `date,rate`) and kept up to date by small, reviewable pull requests.

Each sync either appends the newest fixings or, when there is nothing new (weekends, holidays),
backfills one more year of history back to 2000, so the dataset keeps getting deeper.

## Latest snapshot

<!-- table:start -->
| Pair | Last fixing | Rate | 1d | 20d | 60d vol (ann.) | Rows |
|---|---|---:|---:|---:|---:|---:|
| [EUR/AUD](data/EURAUD.csv) | 2026-10-08 | 1.611 | +0.19% | -0.35% | 4.65% | 197 |
| [EUR/BRL](data/EURBRL.csv) | 2026-10-09 | 5.6086 | -0.06% | -5.33% | 12.39% | 198 |
| [EUR/CAD](data/EURCAD.csv) | 2026-10-08 | 1.5953 | +0.14% | -0.60% | 4.06% | 197 |
| [EUR/CHF](data/EURCHF.csv) | 2026-10-09 | 0.9313 | -0.14% | -1.46% | 5.16% | 198 |
| [EUR/CNY](data/EURCNY.csv) | 2026-10-09 | 7.4992 | +0.03% | -3.56% | 4.39% | 198 |
| [EUR/CZK](data/EURCZK.csv) | 2026-10-08 | 24.403 | -0.10% | +0.63% | 1.71% | 452 |
| [EUR/DKK](data/EURDKK.csv) | 2026-10-07 | 7.4745 | -0.00% | -0.00% | 0.08% | 196 |
| [EUR/GBP](data/EURGBP.csv) | 2026-10-08 | 0.84698 | +0.06% | -1.42% | 2.61% | 197 |
| [EUR/IDR](data/EURIDR.csv) | 2026-10-09 | 20036.94 | -0.04% | -1.80% | 5.17% | 198 |
| [EUR/ILS](data/EURILS.csv) | 2026-10-09 | 3.426 | -0.47% | -2.95% | 7.47% | 198 |
| [EUR/INR](data/EURINR.csv) | 2026-10-08 | 108.2635 | +0.14% | -2.35% | 5.06% | 197 |
| [EUR/ISK](data/EURISK.csv) | 2026-10-08 | 137.0 | +0.00% | -2.14% | 3.75% | 197 |
| [EUR/JPY](data/EURJPY.csv) | 2026-10-09 | 177.34 | +0.16% | -0.68% | 8.31% | 198 |
| [EUR/KRW](data/EURKRW.csv) | 2026-10-09 | 1503.27 | +0.03% | -3.42% | 8.67% | 198 |
| [EUR/MXN](data/EURMXN.csv) | 2026-10-07 | 20.2236 | +0.01% | +2.68% | 6.01% | 196 |
| [EUR/NOK](data/EURNOK.csv) | 2026-10-07 | 10.712 | -0.61% | +0.14% | 4.86% | 196 |
| [EUR/NZD](data/EURNZD.csv) | 2026-10-08 | 2.0014 | +0.19% | +0.37% | 4.90% | 197 |
| [EUR/PHP](data/EURPHP.csv) | 2026-10-07 | 70.203 | -0.71% | -3.59% | 5.44% | 196 |
| [EUR/PLN](data/EURPLN.csv) | 2026-10-09 | 4.3835 | +0.19% | +1.35% | 3.47% | 198 |
| [EUR/SEK](data/EURSEK.csv) | 2026-10-09 | 11.1675 | -0.24% | -0.62% | 3.70% | 198 |
| [EUR/SGD](data/EURSGD.csv) | 2026-10-08 | 1.434 | +0.20% | -2.52% | 2.96% | 197 |
| [EUR/THB](data/EURTHB.csv) | 2026-10-08 | 37.68 | +0.05% | -1.69% | 4.38% | 197 |
| [EUR/TRY](data/EURTRY.csv) | 2026-10-09 | 55.1033 | +0.09% | -2.18% | 4.88% | 198 |
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
