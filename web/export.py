"""Export the analysis into web/data.json (and data.js so the page also works opened as a file).

Counts come from data/summary.json. Store listings, site pitches and the verbatim review
quotes are copied from REPORT.md, where they were recorded on 20 Nov 2026.
Run from the repo root:  python web/export.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
summary = json.load(open(os.path.join(ROOT, "data", "summary.json"), encoding="utf-8"))

REPORT = {
    "listing": {
        "Nova Benefits": {"rating": 3.29, "ratings": 199, "pitch": "24*7 customer support, live claims tracking; raise a claim request in 5 minutes"},
        "Plum": {"rating": 4.72, "ratings": 6399, "pitch": "24/7 helpline, paperless processes, and personal doctor assistance"},
        "Loop Health": {"rating": 4.62, "ratings": 8994, "pitch": "100k+ Claims Passed, 4.8/5"},
        "Pazcare": {"rating": 4.58, "ratings": 3817, "pitch": "Compassionate, efficient claims assistance; NPS score for claims and support"},
        "Onsurity": {"rating": 4.07, "ratings": 7226, "pitch": "Claims model: Good Doctors concierge (compare page, 7 Jul 2026)"},
    },
    "nova_play": {"installs": "50,000+", "version": "2.10.6", "updated": "25 Aug 2026"},
    "nova_appstore": {"rating": 4.13, "ratings": 45, "reviews_read": 21},
    "homepage_claim": "4.7-star rating for 450+ Google Reviews",
    "five_star_in_bursts": 23,
    "examples": {
        "app_login_or_crash": [{"date": "2024-09-09", "text": "While uploading doctor papers app crash mutliple time . Spend 12+hours till now with this app but yet not able to complete my claim submission"},
                               {"date": "2026-06-05", "text": "Keeps signing out. Cannot view scheduled doctor appointments. You cannot recover the ongoing customer support chat window if minimised.", "store": "App Store"}],
        "support_unreachable": [{"date": "2025-05-27", "text": "i tried calling them from early morning 5am till 10am not even connected to customer service in medical emergency"}],
        "claim_slow_or_no_update": [{"date": "2026-10-18", "stars": 1, "text": "After one month also my reimbursement process not yet started. Documents review also not updated."}],
        "claim_rejected": [{"date": "2024-08-31", "text": "They will ask you to upload all the documents then ask again again same documents then in the end will cancel the reimbursement."}],
        "cashless_or_hospital": [{"date": "2024-06-28", "text": "If hospital initiates claim, it is not reflected on app. So, then employee also initiates claim. This results in multiple claims and confusion."}],
        "documents_asked_again": [{"date": "2026-05-27", "text": "They will ask multiple documents even after submission and not in the beginning they ask after 2 months 3 months of claim."},
                                  {"date": "2024-11-05", "text": "after raising this on twitter they finally replied me but asking for more documents", "store": "App Store"}],
        "checkup_or_payment": [{"date": "2026-05-01", "text": "constantly send messages to get annual checkup done , i paid, and no tests for scheduled. they won't refund money as well"}],
    },
    "hand_check": "I read all 44 by hand. 2 tags are borderline (an e-card delay and a check-up technician delay counted as slow). About 4 reviews were missed, for example a step tracker bug.",
    "alert_sample": {"window": "22 Sep to 20 Nov 2026 (60 days)", "new": 2, "avg": 3.0, "low": 1, "not_replied": 1,
                     "item": "2026-10-18 1 star [claim_slow_or_no_update] Very bad experience. After one month also my reimbursement process not yet started.Documents review also not updated."},
    "tests": 11,
}

out = {"summary": summary, "report": REPORT}
W = os.path.join(ROOT, "web")
json.dump(out, open(os.path.join(W, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(W, "data.js"), "w", encoding="utf-8").write("window.DATA = " + json.dumps(out, ensure_ascii=False) + ";\n")
print("ok")
