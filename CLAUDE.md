# Rules for this repo
- Numbers on the dashboard must come from a real pull (OpenSEO / Search Console, Wix API, Metricool). Never estimate; label any judgement as such.
- Task statuses live in scripts/tasks.json (To do / In progress / Done). Keep IDs stable.
- After any change: run `python3 scripts/build_data.py`, check the page renders (desktop + 390px, no sideways scroll), commit and push.
- The page is noindex. Don't add client personal data (names, phones, emails) to it.
