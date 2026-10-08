"""Sync ECB reference rates (EUR base) for one currency into data/EUR<CCY>.csv.

Usage: python3 scripts/sync.py CCY
Prints a JSON summary of what changed (empty "added" if nothing to do).

Strategy: append any fixings newer than the last stored date; if there are
none (weekend / already up to date), backfill the most recent missing year
so the history keeps getting deeper.
"""
import csv
import datetime as dt
import json
import math
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
API = "https://api.frankfurter.app"
EARLIEST = dt.date(2000, 1, 1)


def fetch(start, end, ccy):
    url = f"{API}/{start}..{end}?to={ccy}"
    req = urllib.request.Request(url, headers={"User-Agent": "fx-rates-journal"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    # the API snaps `start` back to the previous business day, so clip to the range
    return {d: v[ccy] for d, v in payload.get("rates", {}).items()
            if ccy in v and str(start) <= d <= str(end)}


def load(path):
    if not path.exists():
        return {}
    with path.open() as f:
        return {row["date"]: float(row["rate"]) for row in csv.DictReader(f)}


def save(path, rows):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "rate"])
        for d in sorted(rows):
            w.writerow([d, rows[d]])


def stats(rows):
    dates = sorted(rows)
    last = rows[dates[-1]]
    def chg(n):
        if len(dates) <= n:
            return None
        return round((last / rows[dates[-1 - n]] - 1) * 100, 2)
    rets = [math.log(rows[b] / rows[a]) for a, b in zip(dates[-61:], dates[-60:])]
    vol = None
    if len(rets) > 2:
        m = sum(rets) / len(rets)
        vol = round(math.sqrt(sum((x - m) ** 2 for x in rets) / (len(rets) - 1) * 252) * 100, 2)
    return {"last_date": dates[-1], "last": last, "chg_1d": chg(1), "chg_20d": chg(20), "vol_60d": vol, "n": len(dates)}


def main(ccy):
    DATA.mkdir(exist_ok=True)
    path = DATA / f"EUR{ccy}.csv"
    rows = load(path)
    today = dt.date.today()
    mode = "update"
    if rows:
        start = dt.date.fromisoformat(max(rows)) + dt.timedelta(days=1)
        new = fetch(start, today, ccy) if start <= today else {}
        new = {d: v for d, v in new.items() if d not in rows}
        if not new:
            first = dt.date.fromisoformat(min(rows))
            if first > EARLIEST:
                mode = "backfill"
                year_start = max(dt.date(first.year - 1, 1, 1), EARLIEST)
                new = fetch(year_start, first - dt.timedelta(days=1), ccy)
    else:
        mode = "init"
        new = fetch(dt.date(today.year, 1, 1), today, ccy)

    rows.update(new)
    if new:
        save(path, rows)
    out = {"ccy": ccy, "mode": mode, "added": sorted(new), "file": str(path.relative_to(ROOT))}
    if rows:
        out["stats"] = stats(rows)
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv[1].upper())
