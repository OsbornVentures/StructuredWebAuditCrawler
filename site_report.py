# core/site_report.py

import os
from urllib.parse import urlparse
from typing import List, Dict
from core.meta_score import compute_sitewide_score

SITES_DIR = "outputs/sites"

def extract_path(url: str) -> str:
    try:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/") or "/"
        return path
    except:
        return "/"

def write_combined_report(domain: str, page_reports: List[Dict]):
    os.makedirs(SITES_DIR, exist_ok=True)
    site_summary = compute_sitewide_score(page_reports)
    report_path = os.path.join(SITES_DIR, f"{domain}.txt")

    verify_json_score = 0
    verify_html_score = 0
    home_score = 0

    for r in page_reports:
        path = extract_path(r.get("url", "").lower())
        score = r.get("backlink_score")
        if score is None:
            continue
        if path in ["/verify", "/verify.html"]:
            verify_html_score = score
        elif path == "/verify.json":
            verify_json_score = score
        elif path == "/":
            home_score = score

    total_backlink_score = (
        min(verify_html_score, 2) +
        min(verify_json_score, 1) +
        min(home_score, 1)
    )

    if total_backlink_score == 4:
        backlink_grade = "🟢 Perfect"
    elif total_backlink_score == 3:
        backlink_grade = "✅ Good Standing"
    elif total_backlink_score == 2:
        backlink_grade = "⚠ Needs Work"
    else:
        backlink_grade = "❌ Not Eligible"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"📡 SITE REPORT — {domain}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Pages Audited: {site_summary['total_pages']}\n")
        f.write(f"Pages Passed: {site_summary['pages_passed']}\n")
        f.write(f"Pages Failed: {site_summary['pages_failed']}\n")
        f.write(f"Average Score: {site_summary['average_score']}\n")
        f.write(f"Mesh Health: {site_summary.get('average_alignment', 0)}% Alignment\n")
        f.write(f"Structured Web Participation: {backlink_grade} ({total_backlink_score}/4)\n\n")

        f.write("Participation Breakdown:\n")
        f.write(f"- /verify.html or /verify: {verify_html_score}/2\n")
        f.write(f"- /verify.json: {verify_json_score}/1\n")
        f.write(f"- / (homepage): {home_score}/1\n\n")

        f.write("Per-Page Scores:\n")
        for i, score in enumerate(site_summary["page_scores"]):
            f.write(f"- Page {i + 1}: {score}\n")

        f.write("\n\n--- AUDIT SUMMARIES ---\n")
        for i, report in enumerate(page_reports):
            f.write(f"\n--- Page {i + 1} ---\n")
            f.write(f"URL: {report.get('url', 'n/a')}\n")
            f.write(f"Status: {report.get('status')}\n")
            f.write(f"Load time: {report.get('load_time_ms', 'n/a')} ms\n")
            f.write(f"Backlink required: {report.get('backlink_required', 'n/a')}\n")
            f.write(f"Backlink found: {report.get('backlink_found', 'n/a')}\n")
            f.write(f"Structured Data: {report.get('structured_data_present', False)}\n")
            f.write(f"Alignment Score: {report.get('alignment_percent', 0)}%\n")
            if isinstance(report.get("backlink_score"), int):
                f.write(f"Backlink Score: {report['backlink_score']}/2 (per page max)\n")
            f.write("Violations:\n")
            if report.get("violations"):
                for v in report["violations"]:
                    f.write(f" - {v}\n")
            else:
                f.write("None ✅\n")

            debug = report.get("debug_log", [])
            if debug:
                f.write("\n--- DEBUG LOG ---\n")
                for line in debug:
                    f.write(f"{line}\n")
