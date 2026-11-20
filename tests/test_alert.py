import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from themes import tag_text  # noqa: E402
from review_alert import build_digest, render, load_csv, main  # noqa: E402

D = dt.date


def row(day, score, text, replied=False):
    return {"id": f"{day}-{score}", "date": D(2026, 11, day), "score": score, "replied": replied, "text": text}


def test_documents_asked_again():
    t = "They will ask you to upload all the documents then ask again again same documents"
    assert "documents_asked_again" in tag_text(t)


def test_rejection_and_slow():
    t = "After one month also my reimbursement process not yet started. Claim rejected."
    tags = tag_text(t)
    assert "claim_rejected" in tags and "claim_slow_or_no_update" in tags


def test_support_unreachable():
    assert "support_unreachable" in tag_text("the customer support system is a joke no one responds")


def test_app_bug():
    assert "app_login_or_crash" in tag_text("Keeps signing out and the app crash on upload")


def test_positive_review_not_tagged():
    assert tag_text("Great experience, really easy to use") == []


def test_empty_text():
    assert tag_text(None) == [] and tag_text("") == []


def test_digest_window_and_counts():
    rows = [row(20, 1, "claim rejected"), row(18, 5, "good"), row(14, 1, "app crash", replied=True),
            row(10, 1, "outside window")]
    d = build_digest(rows, D(2026, 11, 20), days=7)
    assert d["total"] == 3            # 14th, 18th, 20th; 10th is outside
    assert d["negative"] == 2
    assert d["unreplied"] == 1
    assert d["themes"] == {"claim_rejected": 1, "app_login_or_crash": 1}
    assert [r["date"] for r in d["to_answer"]] == [D(2026, 11, 20)]


def test_window_edges():
    rows = [row(13, 1, "x"), row(14, 1, "y")]
    d = build_digest(rows, D(2026, 11, 20), days=7)
    assert d["total"] == 1 and d["to_answer"][0]["date"] == D(2026, 11, 14)


def test_empty_window_renders():
    d = build_digest([], D(2026, 11, 20), days=7)
    out = render(d, "demo")
    assert "New reviews: 0" in out and "Nothing waiting" in out


def test_render_truncates_long_text():
    d = build_digest([row(20, 1, "a" * 400)], D(2026, 11, 20))
    line = [l for l in render(d).splitlines() if l.startswith("- ")][0]
    assert line.endswith("...") and len(line) < 220


def test_csv_round_trip_and_exit_code(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("id,date,score,version,thumbs,replied,text,reply\n"
                 "a,2026-11-19,1,,0,False,documents asked again,\n"
                 "b,2026-11-18,5,,0,True,good,thanks\n", encoding="utf-8")
    rows = load_csv(str(p))
    assert rows[0]["replied"] is False and rows[1]["replied"] is True
    assert main(["--csv", str(p), "--days", "7", "--today", "2026-11-20"]) == 1
    assert main(["--csv", str(p), "--days", "1", "--today", "2026-11-18"]) == 0
