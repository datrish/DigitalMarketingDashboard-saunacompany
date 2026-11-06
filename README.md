# DigitalMarketingDashboard-saunacompany

One-page dashboard for The Sauna Company's SEO, Google local, blog and social work, with a prioritised task list for the marketer.

- `index.html`: the dashboard (reads `data.json`)
- `data.json`: the data snapshot (generated)
- `scripts/build_data.py`: builds `data.json` from the latest pulls
- `scripts/tasks.json`: the task list (ID, priority, owner, status, why, steps)

Data sources: Google Search Console and site audit, rankings, competitors, local map pack and backlinks via OpenSEO; blog via the Wix API; social via Metricool.

To update: refresh the numbers in `scripts/build_data.py`, edit task status in `scripts/tasks.json`, run `python3 scripts/build_data.py`, commit. Vercel redeploys on push.
