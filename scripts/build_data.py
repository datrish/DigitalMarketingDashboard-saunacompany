"""Builds data.json for the dashboard. Snapshot values are pulled from:
OpenSEO (Search Console, site audit, rankings, competitors, local, backlinks), Wix (blog), Metricool (social).
Refresh: re-run the pulls and update the SNAPSHOT dicts below, or let the weekly refresh task do it."""
import json, datetime, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

meta = {"updated": "2026-11-06", "taskSheet": "https://docs.google.com/spreadsheets/d/1p9XYo2lI1HpOhPSk_zDu81XdUJExNkF08fh0tsk6Xns/edit", "gscWindow": "7 Oct – 3 Nov 2026 (28 days)", "site": "saunacompany.co.uk", "trackerApi": "https://script.google.com/macros/s/AKfycbwKzQXb2ung6dtEaDYCPnOaDq9A-5YjUswGa5rXDQrFDYYt5aG01cT-GlRAOXOG2flF/exec",
        "links": {"Task sheet (Ruchi)": "https://docs.google.com/spreadsheets/d/1p9XYo2lI1HpOhPSk_zDu81XdUJExNkF08fh0tsk6Xns/edit", "Search Console": "https://search.google.com/search-console?resource_id=https://www.saunacompany.co.uk/",
                  "OpenSEO project": "https://app.openseo.so/p/8b7fae56-ee74-4da0-91b8-cf245dfb2a41",
                  "Metricool": "https://app.metricool.com/",
                  "Google Business Profile": "https://business.google.com/",
                  "Wix dashboard": "https://manage.wix.com/dashboard/9427eb5f-4e82-46cd-add1-177c68a1f1d2/home",
                  "Wix SEO (redirects)": "https://manage.wix.com/dashboard/9427eb5f-4e82-46cd-add1-177c68a1f1d2/redirects",
                  "Live site": "https://www.saunacompany.co.uk/"}}

kpis = [
  {"label": "Google clicks", "value": 416, "fmt": "int", "prev": 441, "yoy": 423, "note": "last 28 days", "good": "up"},
  {"label": "Google impressions", "value": 30172, "fmt": "int", "prev": 27013, "yoy": 24426, "note": "last 28 days", "good": "up"},
  {"label": "Click-through rate", "value": 1.38, "fmt": "pct", "prev": 1.63, "yoy": 1.73, "note": "clicks ÷ impressions", "good": "up"},
  {"label": "Keywords ranking", "value": 239, "fmt": "int", "note": "UK, any position", "good": "up"},
  {"label": "Google reviews", "value": "3.7★ (3)", "fmt": "text", "note": "Finnmark 4.8★ (52)", "alert": True},
  {"label": "Map pack, 'sauna installation'", "value": "#4", "fmt": "text", "note": "central London search", "good": "up"},
  {"label": "Referring domains", "value": 164, "fmt": "int", "note": "most are low-quality", "alert": True},
  {"label": "Social posts scheduled", "value": 0, "fmt": "int", "note": "next 30 days, Metricool", "alert": True},
]

monthly = [  # Search Console, all devices
  ["Nov 25", 482, 38162], ["Dec 25", 453, 32837], ["Jan 26", 679, 34629], ["Feb 26", 614, 39024],
  ["Mar 26", 625, 40203], ["Apr 26", 461, 26529], ["May 26", 361, 23823], ["Jun 26", 364, 29537],
  ["Jul 26", 373, 35662], ["Aug 26", 415, 35216], ["Sep 26", 473, 30059], ["Oct 26", 488, 32444]]

# Search Console, last 3 months (3 Aug – 3 Nov 2026)
queries = [
  ["the sauna company", 67, 311, 6.1], ["sauna company", 35, 894, 7.2], ["himalayan salt sauna", 14, 447, 4.4],
  ["bespoke sauna uk", 9, 222, 6.4], ["sauna company london", 9, 552, 2.0], ["sauna", 9, 1370, 23.6],
  ["bespoke saunas", 8, 571, 10.2], ["home sauna", 8, 1707, 15.3], ["salt sauna", 8, 578, 8.2],
  ["sauna builders uk", 7, 226, 6.1], ["garage sauna", 6, 121, 4.1], ["sauna installation", 6, 815, 7.4],
  ["sauna installation london", 5, 59, 6.5], ["best home sauna uk", 4, 547, 10.1], ["sauna installation uk", 4, 333, 14.5]]

striking = [  # position 5–20, real impressions: push into the top 5
  ["home sauna", 1707, 15.3, "/  (homepage)"], ["sauna installation", 815, 7.4, "/sauna-installation"],
  ["salt sauna", 578, 8.2, "/bespoke-saunas-london/himalayan-salt-sauna"], ["bespoke saunas", 571, 10.2, "/bespoke-saunas-london"],
  ["best home sauna uk", 547, 10.1, "home sauna comparison post"], ["home saunas", 433, 19.5, "/"],
  ["sauna room", 403, 17.9, "/"], ["sauna builders", 377, 27.1, "/sauna-installation"],
  ["luxury sauna", 371, 19.6, "/bespoke-saunas-london/luxury-home-sauna"], ["bespoke sauna installation", 342, 7.0, "/sauna-installation"],
  ["sauna installation uk", 333, 14.5, "/sauna-installation"], ["sauna cost", 256, 15.5, "cost blog post"],
  ["sauna manufacturers uk", 226, 15.2, "/about-us"], ["sauna design", 187, 10.6, "/sauna-design"]]

pages = [  # url, clicks, impressions, ctr %, position, verdict
  ["/", 740, 42241, 1.75, 16.6, "Rewrite title + description: big audience, low CTR"],
  ["/bespoke-saunas-london/bespoke-steam-rooms", 37, 5476, 0.68, 16.2, "CTR problem: rewrite title, add prices"],
  ["/post/how-much-does-a-sauna-cost-in-the-uk-in-2026", 27, 5523, 0.49, 10.4, "Duplicates the 4 Nov cost post: merge"],
  ["/post/home-sauna-comparison-guide-choosing-the-perfect-sauna-for-your-space", 16, 5231, 0.31, 14.5, "Duplicate of the other comparison post: merge"],
  ["/bespoke-saunas-london", 9, 5110, 0.18, 40.9, "Weak hub page: rebuild"],
  ["/post/home-sauna-comparison-compare-and-choose-the-best-home-sauna-types", 20, 4747, 0.42, 11.6, "Keep one comparison post, redirect the other"],
  ["/post/can-i-put-a-sauna-in-my-garden-shed-the-honest-answer-for-uk-homeowners", 75, 4292, 1.75, 7.9, "Best blog post: link it to /garden-sauna"],
  ["/luxury-outdoor-saunas", 62, 3489, 1.78, 14.6, "Target 'outdoor sauna' (9,900/mo)"],
  ["/bespoke-saunas-london/infrared-sauna", 15, 2902, 0.52, 16.9, "Low CTR: rewrite title"],
  ["/bespoke-saunas-london/himalayan-salt-sauna", 75, 2814, 2.67, 6.3, "Working: push to top 3"],
  ["/bespoke-saunas-london/garden-sauna", 17, 2724, 0.62, 29.4, "Target 'garden sauna' (4,400/mo)"],
  ["/sauna-installation", 8, 2414, 0.33, 29.0, "Money page ranks 29: rewrite first"],
  ["/bespoke-saunas-london/luxury-home-sauna", 18, 2455, 0.73, 22.2, "Strengthen with case studies"],
  ["/bespoke-saunas-london/infrared-red-light-therapy", 19, 2346, 0.81, 24.8, "Target 'red light sauna' (1,300/mo)"],
  ["/bespoke-saunas-london/traditional-finnish-sauna", 19, 2291, 0.83, 20.1, "Target 'finnish sauna' (2,400/mo)"],
  ["/sauna-faq", 2, 1085, 0.18, 38.7, "Add FAQ schema, answer real questions"],
  ["/sauna-prices", 6, 890, 0.67, 45.0, "Competes with cost posts: merge or retarget"],
  ["/bespoke-sauna-case-studies/copy-of-garden-room-hybrid-sauna-bu", 0, 46, 0.0, 52.5, "Duplicate page indexed: delete + redirect"]]

gaps = [  # keyword, UK volume/month, difficulty 0-100, our position (None = not ranking), action
  ["outdoor sauna", 9900, 1, 14.6, "Upgrade /luxury-outdoor-saunas"],
  ["garden sauna", 4400, 1, 29.4, "Upgrade /garden-sauna + link from shed post"],
  ["home sauna uk", 3600, 21, 22.6, "Homepage + home sauna guide"],
  ["finnish sauna", 2400, 12, 40, "Upgrade Finnish sauna page"],
  ["sauna and cold plunge", 1900, 13, None, "New page: Sauna + cold plunge"],
  ["outdoor sauna uk", 1900, 6, None, "Same page as 'outdoor sauna'"],
  ["indoor sauna", 1900, 24, None, "New page: Indoor saunas"],
  ["home steam room", 1300, 0, 16, "Upgrade steam room page"],
  ["red light sauna", 1300, 11, 44, "Upgrade red light page"],
  ["basement sauna", 1000, 0, None, "New page: Basement saunas (low competition)"],
  ["salt sauna", 880, 0, 10, "Already ranking: push to top 3"],
  ["hotel sauna", 720, 0, None, "New page: Commercial saunas"],
  ["bathroom sauna", 320, 0, 31, "New page: Bathroom & en-suite saunas"],
  ["wood fired sauna uk", 320, 0, 23, "Upgrade wood-fired page"],
  ["sauna installation", 210, 0, 7.4, "Rewrite /sauna-installation"],
  ["commercial sauna", 170, 0, None, "New page: Commercial saunas (CPC £6.39)"],
  ["sauna builders", 110, 0, 27.1, "Add to /sauna-installation"],
  ["sauna in garage", 110, 0, 6.3, "Garage case study: add CTA"]]

competitors = [  # domain, SERP visibility (20 core keywords), keywords in top 100, Google rating, reviews, notes
  ["finnmarksauna.com", 5.0, 8, 4.8, 52, "#1 in map pack for 'sauna installation'; big product range"],
  ["polhus.co.uk", 4.25, 6, None, None, "#1 'outdoor sauna uk', #2 'home sauna uk', #1 'garden sauna uk'"],
  ["supersauna.co.uk", 3.2, 7, None, None, "#2 'outdoor sauna uk', #3 'home sauna uk'"],
  ["edenhut.co.uk", 3.05, 6, None, None, "#2 'sauna builders uk', #4 'sauna installation'"],
  ["aqualinesaunas.co.uk", 2.7, 6, None, None, "#1 'sauna installation' and 'sauna installation uk'"],
  ["skotlanti.co.uk", 2.5, 5, None, None, "#1 'sauna builders uk'"],
  ["leisurequip.com", 1.65, 9, None, None, "#2 'home steam room'"],
  ["oceanic-saunas.co.uk", 1.2, 7, None, None, "#1 'home steam room'"],
  ["clearlightsaunas.co.uk", None, None, 5.0, 142, "Map pack #10, 142 reviews"],
  ["sunlighten.com", None, None, 4.9, 166, "Map pack #2, 166 reviews"]]

local = {
  "profile": {"name": "The Sauna Company", "category": "Sauna Shop", "extraCategories": 0, "rating": 3.7, "reviews": 3,
               "ratingSplit": "2 × 5★, 1 × 1★", "photos": 30, "hours": "Mon–Fri 9:00–17:00", "address": "87 Notting Hill Gate, London W11 3JZ",
               "claimed": True, "services": "none listed", "booking": "no booking link", "metricool": "not connected to the sauna brand"},
  "ranks": [["sauna installation", "central London", "#4", "Finnmark #1 (4.8★, 52)"],
            ["bespoke sauna london", "central London", "#11", "results dominated by public saunas and spas"]]}

blog = {
  "total": 27,
  "byMonth": [["Mar 26", 9], ["Apr 26", 7], ["May 26", 7], ["Jun 26", 1], ["Jul 26", 0], ["Aug 26", 0], ["Sep 26", 0], ["Oct 26", 0], ["Nov 26", 3]],
  "top": [["Can I put a sauna in my garden shed?", 210], ["Complete guide to Himalayan salt saunas", 144],
          ["How much does a sauna cost in the UK in 2026?", 119], ["Latest modern luxury sauna trends 2026", 56],
          ["Home sauna comparison guide", 55], ["Garden sauna ideas UK", 46], ["Home sauna comparison: compare and choose", 42]],
  "issues": [
    "Two 'home sauna comparison' posts compete for the same searches (CTR 0.3–0.4%)",
    "Two 'how much does a sauna cost' posts (Mar + 4 Nov) and the /sauna-prices page compete with each other",
    "Three generic 'London sauna services' posts say the same thing (3–12 views each)",
    "No posts for 5 months (June to October), then daily from 3 Nov",
    "11 posts use AI-generated images saved as '-post-ai-image-…png' with no alt text",
    "No categories used; tags are inconsistent"]}

social = {
  "window": "7 Oct – 5 Nov 2026",
  "networks": [["Instagram @sauna_company", 267, "+20", 26, 1446, 575],
               ["Facebook", 142, "+3", 14, 405, 13]],
  "connected": ["Facebook", "Instagram", "Pinterest", "TikTok", "YouTube"],
  "missing": ["Google Business Profile", "LinkedIn"],
  "scheduled": 0}

audit = {"date": "4 Nov 2026", "pages": 100, "rows": [
  ["Slow server response (1.5–3.3 s)", 34, "info"], ["Heading levels skip", 15, "info"],
  ["Missing meta description", 11, "warning"], ["Page is noindex", 11, "info"],
  ["Missing H1", 9, "warning"], ["Title too long", 1, "info"]],
  "note": "Missing H1 / description / noindex are blog tag pages and member profile pages: hide them rather than fix them."}

backlinks = {"domains": 164, "backlinks": 638, "trend": [["Nov 25", 40], ["Jan 26", 55], ["Mar 26", 60], ["May 26", 98], ["Jul 26", 109], ["Sep 26", 141]],
  "good": ["yell.com", "aqua-spazio.co.uk", "getsurrey.co.uk", "locallife.co.uk", "mylocalservices.co.uk"],
  "note": "Most new domains since May 2026 are unrelated foreign sites (e.g. karawanier.com, bannerkencana.com, kingbueno.com). They add little and can look like bought links."}


# ---- Swimming Pool Company (swimmingpoolcompany.co.uk) ----
# Search Console via OpenSEO project d0e87aa8 (pulled 9 Nov 2026); GA4 property 526125024; Wix form submissions + info@ (new people only).
pool = {
  "site": "swimmingpoolcompany.co.uk", "gscWindow": "10 Oct – 6 Nov 2026 (28 days)",
  "kpis": [
    {"label": "Google clicks", "value": 143, "fmt": "int", "prev": 56, "note": "last 28 days", "good": "up"},
    {"label": "Google impressions", "value": 53919, "fmt": "int", "prev": 25878, "note": "last 28 days", "good": "up"},
    {"label": "New leads, October", "value": 2, "fmt": "int", "note": "website form + info@, new people only", "alert": True},
    {"label": "Real (UK) visitors", "value": 154, "fmt": "int", "note": "GA4, 10 Oct–8 Nov, 64% engaged"},
    {"label": "US visitors (bots)", "value": 174, "fmt": "int", "note": "7% engaged, only 2 US Google clicks", "alert": True},
    {"label": "Audit issues that matter", "value": 3, "fmt": "int", "note": "78 pages crawled; rest are tag pages"},
  ],
  "monthly": [  # month, Google clicks, impressions, new leads (forms + info@)
    ["Jun 26", 15, 5210, 1], ["Jul 26", 20, 7133, 2], ["Aug 26", 14, 8467, 6], ["Sep 26", 38, 21062, 4], ["Oct 26", 112, 52642, 2]],
  "queries": [  # last 3 months: query, clicks, impressions, position
    ["the swimming pool company", 21, 206, 2.1], ["swimming pool company", 13, 985, 12.9], ["swimming pool company london", 3, 1049, 6.5],
    ["london swimming pool company", 1, 537, 11.3], ["pool designer london", 1, 478, 16.3], ["swimming pool contractors", 1, 926, 22.1],
    ["bespoke swimming pool design", 0, 459, 2.2], ["basement swimming pool company", 0, 471, 6.3], ["commercial pool contractor london", 0, 456, 13.9]],
  "pages": [  # last 3 months: page, clicks, impressions, position
    ["/", 95, 65551, 23.6], ["/post/cold-plunge-pools-for-uk-homes-benefits-buying-guide", 16, 863, 16.6], ["/outdoor-pool-prices", 13, 4393, 20.0],
    ["/post/how-much-does-an-indoor-swimming-pool-cost-in-the-uk-in-2026", 13, 2877, 19.6], ["/indoor-pool-prices", 6, 1872, 51.5],
    ["/swimming-pool-prices", 2, 4182, 30.5], ["/contact", 3, 5038, 81.7]],
  "sources": [  # GA4 10 Oct – 8 Nov: source, sessions, engagement %
    ["Direct (mostly bots)", 331, 13], ["Google organic", 178, 63], ["ChatGPT", 17, 53], ["LinkedIn", 11, 45], ["Instagram", 16, 56]],
  "findings": [
    "Google clicks more than doubled in the last 28 days (143 vs 56), but new leads stayed at 2–3 a month: visitors arrive but don't enquire.",
    "No commercial pools page: commercial pool searches got ~5,200 impressions at position ~40 and 0 clicks.",
    "Price pages rank too low: /swimming-pool-prices position 30, /indoor-pool-prices position 51.",
    "'bespoke swimming pool design' ranks 2.2 with 459 impressions and 0 clicks: the Google snippet needs rewriting.",
    "US, Singapore and China visits are bots (one visit each, almost no engagement). Judge the site on UK + Google organic only.",
    "Site audit (78 pages): no broken links, orphans or empty pages; only 3 pages with heading-order issues."]}

# Leads per month (new enquiries). Sauna: Wix website forms (may include a few internal tests); Pool: forms + info@, new people only.
leads = {"months": ["Jun", "Jul", "Aug", "Sep", "Oct"], "sauna": [24, 23, 26, 24, 17], "pool": [1, 2, 6, 4, 2],
         "note": "Sauna = Wix website forms (a few may be internal tests). Pool = website form + info@, new people only. No paid ads ran."}

pulse = json.loads((ROOT / "scripts" / "pulse.json").read_text())
tasks = json.loads((ROOT / "scripts" / "tasks.json").read_text())

out = dict(meta=meta, kpis=kpis, monthly=monthly, queries=queries, striking=striking, pages=pages, gaps=gaps,
           competitors=competitors, local=local, blog=blog, social=social, audit=audit, backlinks=backlinks, pool=pool, leads=leads, pulse=pulse, tasks=tasks)
(ROOT / "data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print("data.json written:", len(tasks), "tasks")
