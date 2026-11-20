"""Pull the newest App Store reviews (public RSS, India store) into a CSV. No reviewer names kept."""
import csv, json, sys, urllib.request

def fetch(app_id, out, country="in"):
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/page=1/id={app_id}/sortby=mostrecent/json"
    feed = json.load(urllib.request.urlopen(url, timeout=30))["feed"]
    entries = [e for e in feed.get("entry", []) if "im:rating" in e]  # first entry can be the app itself
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "date", "score", "version", "thumbs", "replied", "text", "reply"])
        for e in entries:
            text = (e["title"]["label"] + ". " + e["content"]["label"]).replace("\n", " ")
            w.writerow([e["id"]["label"], e["updated"]["label"][:10], e["im:rating"]["label"],
                        e.get("im:version", {}).get("label", ""), "", "", text, ""])
    print(app_id, country, "reviews", len(entries))

if __name__ == "__main__":
    fetch(sys.argv[1], sys.argv[2])
