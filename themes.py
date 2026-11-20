"""Complaint themes for group health insurance app reviews.

Keyword rules, not a model. Each rule is a regex run on the lower-cased review text.
A review can hit more than one theme.
"""
import re

THEMES = {
    # Insurer or TPA keeps asking for papers, or asks again for papers already sent
    "documents_asked_again": r"(document|papers|forms?\b).{0,80}(again|multiple|repeated|\d+\s*-?\s*\d*\s*times|missing|after submission|more)"
                             r"|(again|multiple|repeated|more).{0,40}(document|papers)"
                             r"|additional requirement|courier",
    # Claim is slow, stuck or has no update
    "claim_slow_or_no_update": r"(not (yet )?(settled|started|processed|credited|updated))|(claim|process|settle|reimburse)\w*.{0,30}slow|delay|waiting|"
                               r"(\d+|two|three|few)\s*(days?|weeks?|months?)|still (not|they)|lack of updates|no update",
    # Claim rejected or cancelled
    "claim_rejected": r"reject|declin|cancel(led)? the reimburse|claims? (not|never) given|will not let you",
    # Could not reach a person
    "support_unreachable": r"(customer (care|support|service)|support (team|system)|care team|chat|calls?|helpline)"
                           r".{0,60}(no one|not|never|joke|worst|useless|pathetic|no proper|nightmare)"
                           r"|no (proper )?(response|support|reply)|no one responds|not even connected|never connect|not received a (single )?call",
    # App itself broken
    "app_login_or_crash": r"login|log ?out|sign(ing)? (in|out)|password|otp|crash|freez|glitch|not (open|working|moving)|"
                          r"can'?t scroll|stuck on|buggy|slow app|app close|unresponsive|un responsive",
    # Paid add-ons: health check-ups, consults, refunds
    "checkup_or_payment": r"check ?-?up|blood sample|consultation|refund|paid|money gone|payment",
    # Cashless and hospital desk problems
    "cashless_or_hospital": r"cashless|hospital|ambulance|admission|e-?card",
}

_COMPILED = {k: re.compile(v) for k, v in THEMES.items()}


def tag_text(text):
    """Return the sorted list of theme names that match one review text."""
    low = (text or "").lower()
    return sorted(k for k, rx in _COMPILED.items() if rx.search(low))
