# structuredweb_auditor/core/meta_score.py

from typing import List, Dict

def compute_page_score(report: Dict) -> int:
    score = 100

    url = report.get("url", "").lower()
    path = "/" + url.split("/", 3)[-1].split("?", 1)[0].split("#", 1)[0]
    if path in ["/", "/index.html"]:
        path = "/"

    backlink_scored_paths = {"/", "/verify.html", "/verify.json"}

    # 25% — Structured Data (mandatory)
    if not report.get("structured_data_present", False):
        score -= 25

    # 20% — Backlink score (only on root and verify paths)
    if path in backlink_scored_paths:
        backlink_score = report.get("backlink_score")
        if isinstance(backlink_score, int):
            max_backlink_per_page = 2
            penalty = (max_backlink_per_page - backlink_score) * 10
            score -= penalty

    # 25% — Zero Trust (cookies, popups, autoloaded JS)
    if any(
        "cookie" in v.lower() or "popup" in v.lower() or "autoloaded js" in v.lower()
        for v in report.get("violations", [])
    ):
        score -= 25

    # 10% — Load Time (only homepage punished if >1s)
    if path == "/" and report.get("load_time_ms", 0) > 1000:
        score -= 10

    # 10% — Semantic Alignment (proportional penalty below 70%)
    alignment = report.get("alignment_percent", 100)
    if alignment < 70:
        score -= round((70 - alignment) * (10 / 70), 2)

    # 5% — Overall FAIL
    if report.get("status") != "PASS":
        score -= 5

    return max(int(score), 0)


def compute_sitewide_score(page_reports: List[Dict]) -> Dict:
    scores = [compute_page_score(report) for report in page_reports]
    average = round(sum(scores) / len(scores), 2) if scores else 0
    alignment_values = [r.get("alignment_percent", 0) for r in page_reports]
    average_alignment = round(sum(alignment_values) / len(alignment_values), 2) if alignment_values else 0

    return {
        "page_scores": scores,
        "average_score": average,
        "average_alignment": average_alignment,
        "pages_passed": sum(1 for r in page_reports if r.get("status") == "PASS"),
        "pages_failed": sum(1 for r in page_reports if r.get("status") != "PASS"),
        "total_pages": len(scores)
    }
