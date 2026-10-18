# Kentucky Wildcats 2026 Depth Chart

Live site: https://lgw2222.github.io/kentucky-2026-depth-chart/
Owner: Garrott (GitHub lgw2222). One self-contained index.html, no build step.

## What's in the repo
- `index.html` — the whole app (roster, depth chart, live ESPN stats, Game center + box scores, highlights, IG Live, Rankings).
- `draft.json` — 2027 NFL draft board ranks for Kentucky players. Written automatically every morning; don't edit by hand.
- `scripts/update_draft.py` — reads Tankathon's 2027 big board and writes draft.json (Python standard library only).
- `manifest.webmanifest`, `sw.js`, `icons/` — make the site an installable app ("UK Football") with an original wildcat icon. sw.js is network-first: always loads the newest version online, last saved copy offline; ESPN data is never cached.
- `.github/workflows/update-draft.yml` — runs the script daily (~6–7 AM ET) and commits draft.json. "Run workflow" button in the Actions tab runs it on demand.

## How rankings update
- **Kentucky team ranks:** computed in the page from live ESPN box scores on every load.
- **SEC / FBS position ranks:** fetched in the page from ESPN's player stats listings (byathlete), cached in the browser for 6 hours; "Refresh" on the Position ranks tab forces it.
- **NFL draft board:** draft.json from the daily GitHub Action. Players outside Tankathon's board fall back to the consensus ranks stored in index.html (DRAFT27, as of Oct 17, 2026).
- **Reminder:** if draft.json is missing or more than 3 days old, the Rankings button gets an orange dot and the Draft board tab shows how to rerun the update.

## Next steps / notes
- If the Action fails repeatedly, Tankathon probably changed its page layout; update the parser in scripts/update_draft.py.
- Refresh DRAFT27 consensus fallback ranks occasionally.
- ESPN byathlete parsing was built without live testing; confirm the SEC/FBS columns fill in on the live site.
