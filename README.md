# fx-rates-journal

Daily journal of **ECB euro reference rates** for 29 currencies, stored as plain CSV
(`data/EUR<CCY>.csv`, columns `date,rate`) and kept up to date by small, reviewable pull requests.

Each sync either appends the newest fixings or, when there is nothing new (weekends, holidays),
backfills one more year of history back to 2000, so the dataset keeps getting deeper.

## Latest snapshot

<!-- table:start -->
| Pair | Last fixing | Rate | 1d | 20d | 60d vol (ann.) | Rows |
|---|---|---:|---:|---:|---:|---:|
| [EUR/AUD](data/EURAUD.csv) | 2026-11-26 | 1.654 | -0.62% | +4.41% | 6.45% | 232 |
| [EUR/BRL](data/EURBRL.csv) | 2026-11-26 | 6.3272 | -1.95% | +6.23% | 27.31% | 232 |
| [EUR/CAD](data/EURCAD.csv) | 2026-11-26 | 1.5617 | +0.17% | +0.26% | 4.72% | 232 |
| [EUR/CHF](data/EURCHF.csv) | 2026-10-09 | 0.9313 | -0.14% | -1.46% | 5.16% | 198 |
| [EUR/CNY](data/EURCNY.csv) | 2026-10-09 | 7.4992 | +0.03% | -3.56% | 4.39% | 198 |
| [EUR/CZK](data/EURCZK.csv) | 2026-11-26 | 24.453 | +0.07% | +0.48% | 1.95% | 487 |
| [EUR/DKK](data/EURDKK.csv) | 2026-11-26 | 7.4737 | -0.01% | +0.00% | 0.10% | 232 |
| [EUR/GBP](data/EURGBP.csv) | 2026-11-26 | 0.83755 | +0.03% | +0.21% | 2.76% | 232 |
| [EUR/HUF](data/EURHUF.csv) | 2026-11-26 | 372.23 | -0.32% | +1.72% | 6.67% | 232 |
| [EUR/IDR](data/EURIDR.csv) | 2026-10-09 | 20036.94 | -0.04% | -1.80% | 5.17% | 198 |
| [EUR/ILS](data/EURILS.csv) | 2026-10-09 | 3.426 | -0.47% | -2.95% | 7.47% | 198 |
| [EUR/INR](data/EURINR.csv) | 2026-10-08 | 108.2635 | +0.14% | -2.35% | 5.06% | 197 |
| [EUR/ISK](data/EURISK.csv) | 2026-11-26 | 137.0 | -0.15% | +0.88% | 3.46% | 232 |
| [EUR/JPY](data/EURJPY.csv) | 2026-11-26 | 174.79 | +0.33% | -0.64% | 6.52% | 232 |
| [EUR/KRW](data/EURKRW.csv) | 2026-11-26 | 1475.75 | +0.31% | -0.85% | 8.48% | 232 |
| [EUR/MXN](data/EURMXN.csv) | 2026-10-07 | 20.2236 | +0.01% | +2.68% | 6.01% | 196 |
| [EUR/MYR](data/EURMYR.csv) | 2026-11-26 | 4.519 | +0.32% | +0.02% | 4.96% | 232 |
| [EUR/NOK](data/EURNOK.csv) | 2026-11-26 | 10.718 | -0.55% | +3.74% | 6.14% | 232 |
| [EUR/NZD](data/EURNZD.csv) | 2026-10-09 | 1.9961 | -0.26% | +0.24% | 4.94% | 198 |
| [EUR/PHP](data/EURPHP.csv) | 2026-10-07 | 70.203 | -0.71% | -3.59% | 5.44% | 196 |
| [EUR/PLN](data/EURPLN.csv) | 2026-10-09 | 4.3835 | +0.19% | +1.35% | 3.47% | 198 |
| [EUR/RON](data/EURRON.csv) | 2026-11-26 | 5.344 | +0.02% | -0.00% | 2.87% | 232 |
| [EUR/SEK](data/EURSEK.csv) | 2026-11-26 | 11.2025 | -0.32% | +1.85% | 4.23% | 232 |
| [EUR/SGD](data/EURSGD.csv) | 2026-11-26 | 1.4163 | +0.24% | -0.72% | 3.55% | 232 |
| [EUR/THB](data/EURTHB.csv) | 2026-10-08 | 37.68 | +0.05% | -1.69% | 4.38% | 197 |
| [EUR/TRY](data/EURTRY.csv) | 2026-10-09 | 55.1033 | +0.09% | -2.18% | 4.88% | 198 |
| [EUR/ZAR](data/EURZAR.csv) | 2026-11-26 | 19.2646 | -0.45% | +4.01% | 7.30% | 232 |
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
