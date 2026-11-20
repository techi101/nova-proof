"""Weekly review-theme alert for a Play Store app.

Pulls (or reads) reviews, keeps the last N days, tags the 1 and 2 star ones with
complaint themes and lists the ones nobody has replied to yet. Output is plain
markdown that can be pasted into Slack or email.

  python review_alert.py --app com.novabenefits --days 7
  python review_alert.py --csv data/nova_play.csv --days 30 --today 2026-11-20

Exit code is 1 when there are unreplied negative reviews in the window, so a
scheduler (cron, GitHub Actions, Task Scheduler) can treat it as "needs a look".
"""
import argparse
import csv
import datetime as dt
import sys
from collections import Counter

from themes import tag_text


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["date"] = dt.date.fromisoformat(r["date"])
        r["score"] = int(r["score"])
        r["replied"] = str(r.get("replied", "")).strip().lower() == "true"
    return rows


def fetch_live(app_id, n=500):
    from google_play_scraper import reviews, Sort  # imported here so tests need no network
    batch, _ = reviews(app_id, lang="en", country="in", sort=Sort.NEWEST, count=n)
    return [{"id": b["reviewId"], "date": b["at"].date(), "score": b["score"],
             "replied": bool(b.get("replyContent")), "text": (b["content"] or "").replace("\n", " ")}
            for b in batch]


def build_digest(rows, today, days=7):
    """Summarise reviews dated in (today - days, today]."""
    start = today - dt.timedelta(days=days)
    window = [r for r in rows if start < r["date"] <= today]
    neg = [dict(r, themes=tag_text(r["text"])) for r in window if r["score"] <= 2]
    unreplied = [r for r in neg if not r["replied"]]
    themes = Counter(t for r in neg for t in r["themes"])
    return {
        "from": start + dt.timedelta(days=1), "to": today, "days": days,
        "total": len(window), "negative": len(neg), "unreplied": len(unreplied),
        "avg_score": round(sum(r["score"] for r in window) / len(window), 2) if window else None,
        "themes": dict(themes.most_common()),
        "untagged": sum(1 for r in neg if not r["themes"]),
        "to_answer": sorted(unreplied, key=lambda r: r["date"]),
    }


def render(d, app_label="app"):
    lines = [f"Review alert for {app_label}: {d['from']} to {d['to']} ({d['days']} days)",
             f"New reviews: {d['total']} | average stars: {d['avg_score'] if d['avg_score'] is not None else 'n/a'}"
             f" | 1-2 star: {d['negative']} | not replied: {d['unreplied']}"]
    if d["themes"]:
        lines.append("Themes in 1-2 star reviews: " + ", ".join(f"{k} {v}" for k, v in d["themes"].items())
                     + (f", untagged {d['untagged']}" if d["untagged"] else ""))
    if d["to_answer"]:
        lines.append("Reply to these:")
        for r in d["to_answer"]:
            text = r["text"] if len(r["text"]) <= 160 else r["text"][:157] + "..."
            tags = ",".join(r["themes"]) or "untagged"
            lines.append(f"- {r['date']} {r['score']} star [{tags}] {text}")
    else:
        lines.append("Nothing waiting for a reply.")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--app", help="Play package id, fetched live")
    src.add_argument("--csv", help="CSV with id,date,score,replied,text columns")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    a = p.parse_args(argv)
    rows = fetch_live(a.app) if a.app else load_csv(a.csv)
    d = build_digest(rows, a.today, a.days)
    sys.stdout.reconfigure(encoding="utf-8")
    print(render(d, a.app or a.csv))
    return 1 if d["unreplied"] else 0


if __name__ == "__main__":
    sys.exit(main())
