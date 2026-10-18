#!/usr/bin/env python3
"""Daily draft-board updater for the Kentucky 2026 depth chart.

Reads Tankathon's 2027 NFL Draft Big Board, keeps every Kentucky player on it,
and writes draft.json next to index.html. Standard library only.
If the page can't be read or looks wrong, it exits with an error and leaves
the old draft.json alone (the site then shows a reminder after a few days).
"""
import html, json, re, sys, urllib.request
from datetime import datetime, timezone

URL = "https://www.tankathon.com/nfl/big-board"
SCHOOL = "Kentucky"
OUT = "draft.json"

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; uk-depth-chart-updater/1.0; +https://lgw2222.github.io/kentucky-2026-depth-chart/)",
        "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def text_of(fragment):
    t = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

def parse(page):
    page = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", page)
    # Only the overall board: stop where the later-year / by-school sections begin.
    cut = re.search(r"(?i)2028\s+NFL\s+DRAFT", page)
    body = page[:cut.start()] if cut else page
    players, seen, last_end = [], set(), 0
    for m in re.finditer(r'(?is)<a[^>]+href="[^"]*/nfl/players/([a-z0-9\-]+)"[^>]*>(.*?)</a>', body):
        slug, inner = m.group(1), text_of(m.group(2))
        between = text_of(body[last_end:m.start()])
        last_end = m.end()
        if slug in seen or "|" not in inner:
            continue
        seen.add(slug)
        left, school = [s.strip() for s in inner.rsplit("|", 1)]
        parts = left.split(" ")
        pos, name = parts[-1], " ".join(parts[:-1])
        nums = re.findall(r"(?:^|\s)(\d{1,4}|NR)(?=\s|$)", between)
        rank = nums[-1] if nums else None
        rank = int(rank) if rank and rank.isdigit() else None
        players.append({"name": name, "pos": pos, "school": school, "rank": rank, "slug": slug})
    return players

def main():
    try:
        players = parse(fetch(URL))
    except Exception as e:
        sys.exit(f"Couldn't read the big board: {e}")
    ranked = [p for p in players if p["rank"]]
    if len(ranked) < 50:
        sys.exit(f"Big board looked wrong (only {len(ranked)} ranked players found); keeping the old draft.json.")
    uk = {p["name"]: {"rank": p["rank"], "pos": p["pos"], "url": f"https://www.tankathon.com/nfl/players/{p['slug']}"}
          for p in players if p["school"] == SCHOOL}
    out = {
        "source": "Tankathon 2027 NFL Draft Big Board",
        "sourceUrl": URL,
        "checked": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boardSize": max(p["rank"] for p in ranked),
        "players": uk,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Saved {len(uk)} Kentucky players from a {out['boardSize']}-player board: " +
          ", ".join(f"{n} #{v['rank'] or 'NR'}" for n, v in uk.items()))

if __name__ == "__main__":
    main()
