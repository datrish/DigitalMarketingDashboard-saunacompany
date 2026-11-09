"""Rebuild scripts/tasks.json from Ruchi's task tracker (Google Sheet).

Source of truth: "Ruchi – Leads & Website Task Tracker (Nov 2026)"
https://docs.google.com/spreadsheets/d/1p9XYo2lI1HpOhPSk_zDu81XdUJExNkF08fh0tsk6Xns/edit

Usage:
  1. Export the Tasks tab as CSV (File > Download > CSV, or the Drive API export,
     which exports the first tab - Tasks is the first tab).
  2. python3 scripts/sync_tasks_from_tracker.py path/to/tasks.csv
  3. python3 scripts/build_data.py
IDs stay stable (they come from the sheet's ID column).
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PRIORITY = {"1 - High": "Urgent", "2 - Medium": "High", "3 - Low": "Medium"}
STATUS = {"Not started": "To do", "In progress": "In progress", "Done": "Done",
          "Blocked": "Blocked", "Needs Deepti": "Needs Deepti"}


def steps_from(detail: str):
    parts = [p.strip() for p in detail.replace(" ; ", ";").split(";")]
    return [p for p in parts if p]


def main(path: str):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    tasks = []
    for r in rows:
        tid = (r.get("ID") or "").strip()
        if not tid:
            continue
        note = (r.get("Ruchi's notes / proof link") or "").strip()
        why = (r.get("Why (source)") or "").strip()
        tasks.append({
            "id": tid,
            "priority": PRIORITY.get(r.get("Priority", "").strip(), "Medium"),
            "area": r.get("Area", "").strip(),
            "site": r.get("Site", "").strip(),
            "owner": "Ruchi",
            "status": STATUS.get(r.get("Status", "").strip(), "To do"),
            "due": r.get("Target date", "").strip(),
            "done_on": r.get("Date done", "").strip(),
            "title": r.get("Task", "").strip(),
            "why": why,
            "steps": steps_from(r.get("Pages / detail", "")),
            "notes": note,
        })
    out = ROOT / "scripts" / "tasks.json"
    out.write_text(json.dumps(tasks, indent=1, ensure_ascii=False) + "\n")
    print("tasks.json written:", len(tasks), "tasks")


if __name__ == "__main__":
    main(sys.argv[1])
