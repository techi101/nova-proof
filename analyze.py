"""Nova Benefits review analysis plus a Play Store comparison with Plum, Loop, Onsurity and Pazcare.

Reads the CSVs in data/ (made by fetch.py) and writes data/summary.json.
"""
import json
import sys
import datetime as dt
from collections import Counter

from review_alert import load_csv
from themes import tag_text, THEMES

sys.stdout.reconfigure(encoding="utf-8")
SNAPSHOT = dt.date(2026, 11, 20)
APPS = {
    "Nova Benefits": "data/nova_play.csv",
    "Plum": "data/comp_com.plumhq.employee.production.csv",
    "Loop Health": "data/comp_com.invoqhealth.loophealth.patient.csv",
    "Onsurity": "data/comp_com.onsurity.csv",
    "Pazcare": "data/comp_com.getpaz.pazcare.csv",
}


def pct(a, b):
    return round(100 * a / b, 1) if b else None


def app_stats(rows, since):
    recent = [r for r in rows if r["date"] >= since]
    neg = [r for r in recent if r["score"] <= 2]
    tags = Counter(t for r in neg for t in tag_text(r["text"]))
    return {
        "text_reviews_all_time": len(rows),
        "oldest": str(min(r["date"] for r in rows)),
        "last_12m_reviews": len(recent),
        "last_12m_neg": len(neg),
        "last_12m_neg_pct": pct(len(neg), len(recent)),
        "last_12m_neg_replied": sum(r["replied"] for r in neg),
        "last_12m_neg_reply_pct": pct(sum(r["replied"] for r in neg), len(neg)),
        "last_12m_neg_theme_pct": {k: pct(tags[k], len(neg)) for k in THEMES},
    }


def nova_detail(rows):
    neg = [r for r in rows if r["score"] <= 2]
    long_neg = [r for r in neg if len(r["text"].split()) >= 6]  # skip "very bad" one-liners
    tags = Counter(t for r in long_neg for t in tag_text(r["text"]))
    replied = sorted(r["date"] for r in rows if r["replied"])
    last_reply = replied[-1] if replied else None
    neg_after = [r for r in neg if last_reply and r["date"] > last_reply]
    by_year = {}
    for r in rows:
        y = by_year.setdefault(r["date"].year, {"n": 0, "neg": 0, "stars": 0})
        y["n"] += 1; y["neg"] += r["score"] <= 2; y["stars"] += r["score"]
    for y in by_year.values():
        y["avg"] = round(y.pop("stars") / y["n"], 2)
    # same-week bursts of 5 star reviews (hint of a review ask after good claims)
    weeks = Counter((r["date"] - dt.timedelta(days=r["date"].weekday())) for r in rows if r["score"] == 5)
    return {
        "neg_total": len(neg), "neg_descriptive": len(long_neg),
        "theme_counts_descriptive_neg": {k: tags[k] for k in THEMES},
        "untagged_descriptive_neg": sum(1 for r in long_neg if not tag_text(r["text"])),
        "replies_total": len(replied), "first_reply": str(replied[0]) if replied else None,
        "last_reply": str(last_reply) if last_reply else None,
        "neg_after_last_reply": len(neg_after),
        "by_year": {str(k): v for k, v in sorted(by_year.items())},
        "five_star_weeks_with_3plus": {str(k): v for k, v in sorted(weeks.items()) if v >= 3},
        "five_star_total": sum(weeks.values()),
    }


def main():
    since = SNAPSHOT - dt.timedelta(days=365)
    data = {k: load_csv(v) for k, v in APPS.items()}
    out = {"snapshot": str(SNAPSHOT), "window_12m_from": str(since),
           "apps": {k: app_stats(v, since) for k, v in data.items()},
           "nova": nova_detail(data["Nova Benefits"])}
    json.dump(out, open("data/summary.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
