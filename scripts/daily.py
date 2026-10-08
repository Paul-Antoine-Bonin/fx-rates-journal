"""Daily job: open and merge one PR per currency sync (10-20 per run).

Usage: python3 scripts/daily.py [--min 10] [--max 20] [--dry-run]
Requires git + an authenticated `gh` CLI.
"""
import argparse
import csv
import datetime as dt
import json
import random
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import sync  # noqa: E402
CURRENCIES = [
    "USD", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "SEK", "NOK", "DKK",
    "PLN", "CZK", "HUF", "RON", "TRY", "CNY", "HKD", "SGD", "KRW", "INR",
    "IDR", "MYR", "PHP", "THB", "ILS", "ZAR", "MXN", "BRL", "ISK",
]
START, END = "<!-- table:start -->", "<!-- table:end -->"


def sh(*cmd):
    r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def fmt(x, suffix="%"):
    return "–" if x is None else f"{x:+.2f}{suffix}" if suffix == "%" else f"{x:.2f}%"


def render_table():
    lines = ["| Pair | Last fixing | Rate | 1d | 20d | 60d vol (ann.) | Rows |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for path in sorted((ROOT / "data").glob("EUR*.csv")):
        out = sync.stats(sync.load(path))
        pair = f"EUR/{path.stem[3:]}"
        lines.append(f"| [{pair}](data/{path.name}) | {out['last_date']} | {out['last']} | "
                     f"{fmt(out['chg_1d'])} | {fmt(out['chg_20d'])} | {fmt(out['vol_60d'], '')} | {out['n']} |")
    readme = ROOT / "README.md"
    text = readme.read_text()
    a, b = text.index(START) + len(START), text.index(END)
    readme.write_text(text[:a] + "\n" + "\n".join(lines) + "\n" + text[b:])


def pr_text(res):
    ccy, mode, added, st = res["ccy"], res["mode"], res["added"], res["stats"]
    span = f"{added[0]} → {added[-1]}" if len(added) > 1 else added[0]
    if mode == "backfill":
        title = f"data(EUR{ccy}): backfill {added[0][:4]} ECB fixings"
    elif mode == "init":
        title = f"data(EUR{ccy}): add EUR/{ccy} series"
    else:
        title = f"data(EUR{ccy}): sync fixings through {added[-1]}"
    body = (
        f"Automated sync of ECB reference rates for **EUR/{ccy}**.\n\n"
        f"- Mode: `{mode}`\n- Rows added: **{len(added)}** ({span})\n"
        f"- Latest fixing: {st['last_date']} = `{st['last']}`\n"
        f"- 1d: {fmt(st['chg_1d'])} · 20d: {fmt(st['chg_20d'])} · 60d vol: {fmt(st['vol_60d'], '')}\n\n"
        "Source: ECB via frankfurter.app. README table regenerated."
    )
    return title, body


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--min", type=int, default=10)
    p.add_argument("--max", type=int, default=20)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    target = random.randint(a.min, a.max)
    pool = CURRENCIES[:]
    random.shuffle(pool)
    done = 0
    print(f"target: {target} PRs")
    for ccy in pool:
        if done >= target:
            break
        sh("git", "checkout", "-q", "main")
        sh("git", "pull", "-q", "--ff-only")
        res = json.loads(sh(sys.executable, "scripts/sync.py", ccy))
        if not res["added"]:
            continue
        render_table()
        title, body = pr_text(res)
        branch = f"data/eur{ccy.lower()}-{res['mode']}-{res['added'][-1]}"
        if a.dry_run:
            print("[dry-run]", title)
            sh("git", "checkout", "-q", "--", ".")
            sh("git", "clean", "-qfd", "data")
            done += 1
            continue
        sh("git", "checkout", "-q", "-b", branch)
        sh("git", "add", "data", "README.md")
        sh("git", "commit", "-q", "-m", title)
        sh("git", "push", "-q", "-u", "origin", branch)
        url = sh("gh", "pr", "create", "--title", title, "--body", body, "--base", "main", "--head", branch)
        sh("gh", "pr", "merge", url, "--squash", "--delete-branch", "--body", body + "\n\nCo-authored-by: ASRIDK <68287121+ASRIDK@users.noreply.github.com>")
        sh("git", "checkout", "-q", "main")
        done += 1
        print(f"[{done}/{target}] merged {url}  {title}", flush=True)
        if done < target:
            time.sleep(random.uniform(15, 45))
    sh("git", "checkout", "-q", "main")
    sh("git", "pull", "-q", "--ff-only")
    print(f"done: {done} PRs merged on {dt.date.today()}")


if __name__ == "__main__":
    main()
