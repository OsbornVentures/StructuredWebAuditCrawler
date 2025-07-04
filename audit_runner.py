# structuredweb_auditor/core/audit_runner.py

import os
import requests
from urllib.parse import urlparse
from typing import Tuple

from rules.performance import audit_performance
from rules.schema import audit_schema
from rules.trust import audit_backlink
from rules.zero_trust import audit_zero_trust
from rules.semantic_alignment import audit_semantic_alignment
from core.report_writer import write_page_report, write_raw_schema

OUTPUT_DIR = "outputs/pages"
RAW_SCHEMA_DIR = "outputs/pages/raw_schema"

def fetch_page(url: str) -> Tuple[str, str]:
    headers = {"User-Agent": "StructuredWebAuditor/1.0"}
    response = requests.get(url, headers=headers, timeout=10)
    return response.text, response.url

def sanitize_slug(url: str) -> str:
    parsed = urlparse(url)
    slug = parsed.path.strip("/").replace("/", "-") or "home"
    return f"{parsed.netloc.replace('.', '_')}-{slug}"

def ensure_output_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(RAW_SCHEMA_DIR, exist_ok=True)

def audit_page(url: str) -> dict:
    try:
        html_content, final_url = fetch_page(url)
    except Exception as e:
        return {
            "url": url,
            "status": "FAIL",
            "violations": [f"Failed to fetch URL: {str(e)}"]
        }

    # Run audits
    perf = audit_performance(final_url, html_content)
    schema = audit_schema(final_url, html_content)
    trust = audit_backlink(final_url, html_content)
    zero = audit_zero_trust(final_url, html_content)
    alignment = audit_semantic_alignment(
        html=html_content,
        json_ld_blocks=schema.get("json_ld_data", []),
        microdata_items=schema.get("microdata_data", [])
    )

    slug = sanitize_slug(final_url)
    ensure_output_dirs()

    all_pass = all([
        perf["status"] == "PASS",
        schema["status"] == "PASS",
        trust["status"] == "PASS",
        zero["status"] == "PASS"
    ])

    is_json_page = final_url.lower().endswith(".json")
    structured_ok = schema.get("has_json_ld", False)

    summary = {
    "url": final_url,
    "status": "PASS" if all_pass else "FAIL",
    "load_time_ms": perf.get("load_time_ms"),
    "backlink_required": trust.get("required"),
    "backlink_found": trust.get("backlink_found"),
    "backlink_score": trust.get("backlink_score", 0),
    "alignment_percent": alignment.get("alignment_percent", 0),
    "structured_data_present": schema.get("has_json_ld", False),
    "violations": (
        perf.get("violations", [])
        + schema.get("violations", [])
        + trust.get("violations", [])
        + zero.get("violations", [])
        + [f"Missing structured keyword: {term}" for term in alignment.get("missing_terms", [])]
    )
}
    write_page_report(slug, final_url, summary, schema, alignment, debug_logs=zero.get("debug_log", []))
    write_raw_schema(slug, schema.get("json_ld_data", []))

    return summary
