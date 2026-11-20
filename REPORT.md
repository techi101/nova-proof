# Nova Benefits: what the app reviews say, and a small tool to watch them

Snapshot: 20 Nov 2026. Everything below comes from public pages read that day. Numbers are counts, not guesses.

## Why I looked at this
Saransh Garg's Founder's Office post (13 Nov 2026) asks for someone who can "identify operational inefficiencies", work on "customer experience", and has "independently built a useful tool, automation, or workflow using AI". Nova's own pages promise "24*7 customer support" and "live claims tracking". App store reviews are the one place where employees (not HR buyers) talk about Nova in public, so I started there.

## The data
| Source | What I got |
|---|---|
| Google Play, com.novabenefits (India, English) | All 107 text reviews, 3 Mar 2021 to 4 Nov 2026. Listing: 3.29 stars, 199 ratings, 50,000+ installs, version 2.10.6 (updated 25 Aug 2026). |
| App Store, id 1561333321 (India) | 21 newest reviews from the public feed. Listing: 4.13 stars from 45 ratings. |
| Plum, Loop Health, Onsurity, Pazcare on Google Play | Every text review the store returned: 1,796 / 863 / 1,196 / 423. |

Small sample warning: Nova has 107 Play reviews in total and 15 in the last 12 months. Treat Nova percentages as direction, not precision. Nova's users are employees of client companies, not retail buyers, so few of them review.

## Finding 1: negative reviews on Play have had no reply since July 2022
* Nova replied to 5 Play reviews, all between 18 Jun and 21 Jul 2022.
* Since 21 Jul 2022, 48 reviews at 1 or 2 stars have been posted. None has a reply.
* Last 12 months (20 Nov 2025 to 20 Nov 2026), 1 to 2 star reviews with a developer reply:

| App | 1-2 star, last 12 months | Replied | Rate |
|---|---|---|---|
| Pazcare | 44 | 40 | 91% |
| Loop Health | 69 | 55 | 80% |
| Plum | 87 | 54 | 62% |
| Onsurity | 86 | 8 | 9% |
| Nova Benefits | 7 | 0 | 0% |

The newest one (18 Oct 2026, 1 star): "After one month also my reimbursement process not yet started. Documents review also not updated." Any HR buyer comparing Nova with Plum or Pazcare can open this public page. Nova's homepage leads with "4.7-star rating for 450+ Google Reviews", while the Play listing sits at 3.29.

## Finding 2: what the complaints are about
44 of Nova's 56 one and two star Play reviews have six or more words. Keyword rules (themes.py) tagged them; a review can have several themes.

| Theme | Of 44 | Example, verbatim |
|---|---|---|
| App login, sign out, crash | 12 | "While uploading doctor papers app crash mutliple time . Spend 12+hours till now with this app but yet not able to complete my claim submission" (9 Sep 2024) |
| Could not reach support | 9 | "i tried calling them from early morning 5am till 10am not even connected to customer service in medical emergency" (27 May 2025) |
| Claim slow or no update | 8 | "After one month also my reimbursement process not yet started." (18 Oct 2026) |
| Claim rejected | 8 | "They will ask you to upload all the documents then ask again again same documents then in the end will cancel the reimbursement." (31 Aug 2024) |
| Cashless or hospital | 6 | "If hospital initiates claim, it is not reflected on app. So, then employee also initiates claim. This results in multiple claims and confusion." (28 Jun 2024) |
| Documents asked again | 4 | "They will ask multiple documents even after submission and not in the beginning they ask after 2 months 3 months of claim." (27 May 2026) |
| Paid check-ups, refunds | 4 | "constantly send messages to get annual checkup done , i paid, and no tests for scheduled. they won't refund money as well" (1 May 2026) |
| None of the above | 7 | |

App Store echoes:
* 5 Nov 2024: "after raising this on twitter they finally replied me but asking for more documents".
* 5 Jun 2026: "Keeps signing out. Cannot view scheduled doctor appointments. You cannot recover the ongoing customer support chat window if minimised."

"Documents asked again" is rare at competitors in the last 12 months: Plum 3 of 87, Onsurity 2 of 86, Loop and Pazcare 0. Nova has 4 of 44 across all years and 1 of 7 in the last year. The numbers are small, but in the reviews above this is the theme that turns a slow claim into a rejected one.

Rule check: I read all 44 by hand. 2 tags are borderline (an e-card delay and a check-up technician delay counted as "slow"). About 4 reviews were missed, for example a step tracker bug.

## Finding 3: happy reviews arrive in bursts
23 of 44 five-star Play reviews fall in 7 weeks that each have 3 or more, for example 4 in the week of 9 Feb 2026. Several name a Nova claims person. This looks like a review request after a good claim, which is a good habit. Unhappy users get no reply and no visible route to a person, so they go to the store.

## Competitor teardown
| | Pitch on own site (20 Nov 2026) | Play rating, ratings | Reply rate, 1-2 star, 12 months |
|---|---|---|---|
| Plum | "24/7 helpline, paperless processes, and personal doctor assistance" | 4.72, 6,399 | 62% |
| Loop Health | "100k+ Claims Passed", "4.8/5" | 4.62, 8,994 | 80% |
| Pazcare | "Compassionate, efficient claims assistance", "NPS score for claims and support" | 4.58, 3,817 | 91% |
| Onsurity | Compare page (as of 7 Jul 2026): claims model "Good Doctors concierge" | 4.07, 7,226 | 9% |
| Nova Benefits | "24*7 customer support, live claims tracking", "Raise a claim request in 5 minutes" | 3.29, 199 | 0% |

Every competitor sells the claims experience. The three with the best store ratings also answer most of their unhappy reviews.

## Recommendations
1. **Answer every 1 to 2 star review within 2 working days, starting with the 18 Oct 2026 one.** It costs almost nothing and turns silence into proof of the "24*7 support" promise. Measure: reply rate (now 0%) and the rating trend.
2. **One complete document list per claim.** Track "times documents requested per claim" and aim for one. This needs the insurer or TPA side too.
3. **Fix the sign-out and lost-chat bugs first.** They are the biggest theme (12 of 44). A user who loses the chat is the user who writes the review.
4. **Run the weekly alert below** so reviews reach ops without anyone opening the store console.

## What I built: review_alert.py
A weekly digest for any Play app. It pulls new reviews, tags the 1 to 2 star ones by theme, and lists every one without a reply. Exit code 1 means "something needs a reply", so it can run on a scheduler and post to Slack or email.

    python review_alert.py --app com.novabenefits --days 7

Sample on the snapshot (--csv data/nova_play.csv --days 60 --today 2026-11-20):

    Review alert for data/nova_play.csv: 2026-09-22 to 2026-11-20 (60 days)
    New reviews: 2 | average stars: 3.0 | 1-2 star: 1 | not replied: 1
    Themes in 1-2 star reviews: claim_slow_or_no_update 1
    Reply to these:
    - 2026-10-18 1 star [claim_slow_or_no_update] Very bad experience. After one month also my reimbursement process not yet started.Documents review also not updated.

Tests: `python -m pytest -q tests` (11 pass, no network).

Rebuild:
1. `pip install google-play-scraper pytest`
2. `python fetch.py com.novabenefits 5000 data/nova_play.csv`, and the same for the four competitor ids listed in analyze.py.
3. `python analyze.py`

A new fetch will give slightly different numbers.

## Limits
* Play reviews are a small, self-selected sample. They are employees' own accounts, not claim records.
* Theme tags are keyword rules, hand-checked on Nova only.
* The reply check sees only replies shown on the store page. Nova may contact users by email or phone.
* AmbitionBox and Glassdoor pages could not be read.

## Sources
* Founder's Office post, 13 Nov 2026: https://www.linkedin.com/posts/saranshatnovabenefits_nova-benefits-is-hiring-for-the-founders-activity-7526886219696230400-yL9G (apply link: https://novabenefits.zohorecruit.in/jobs/Careers/47131000004060047/Founder-s-Office)
* Profitability post, 17 Mar 2026: https://www.linkedin.com/posts/saranshatnovabenefits_nova-benefits-achieves-profitability-milestone-activity-7439580514535182336-Vhdb
* https://www.novabenefits.com/ and https://www.novabenefits.com/employer-experience
* Play: com.novabenefits, com.plumhq.employee.production, com.invoqhealth.loophealth.patient, com.onsurity, com.getpaz.pazcare
* App Store: https://apps.apple.com/in/app/nova-benefits/id1561333321
* https://www.plumhq.com/ , https://www.loophealth.com/ , https://www.pazcare.com/ , https://www.onsurity.com/compare
