# core/report_writer.py

import os
import json
from typing import Dict, List

OUTPUT_DIR = "outputs/pages"
RAW_SCHEMA_DIR = "outputs/pages/raw_schema"

def write_page_report(slug: str, final_url: str, summary: Dict, schema: Dict, alignment: Dict, debug_logs: List[str] = None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(RAW_SCHEMA_DIR, exist_ok=True)

    report_path = os.path.join(OUTPUT_DIR, f"{slug}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"URL: {final_url}\n")
        f.write("Raw JSON-LD:\n")
        f.write(json.dumps(schema["json_ld_data"], indent=2, ensure_ascii=False))

        f.write("\n\n--- AUDIT SUMMARY ---\n")
        f.write(f"Status: {summary['status']}\n")
        f.write(f"Load time: {summary['load_time_ms']} ms\n")
        f.write(f"Backlink required: {summary['backlink_required']}\n")
        f.write(f"Backlink found: {summary['backlink_found']}\n")
        f.write(f"Alignment %: {summary['alignment_percent']}%\n")
        f.write(f"Structured data present (JSON-LD): {summary['structured_data_present']}\n\n")

        f.write("Violations:\n")
        if summary["violations"]:
            for v in summary["violations"]:
                f.write(f"- {v}\n")
        else:
            f.write("None\n")

        f.write("\nSemantic Terms (shared):\n")
        for term in alignment.get("shared_terms", []):
            f.write(f"✔ {term}\n")

        f.write("\nSemantic Terms (missing):\n")
        for term in alignment.get("missing_terms", []):
            f.write(f"✘ {term}\n")

        f.write("\nRaw Microdata:\n")
        for md in schema["microdata_data"]:
            f.write(md.get("html", "") + "\n")

        if debug_logs:
            f.write("\n--- Zero Trust Debug ---\n")
            for line in debug_logs:
                f.write(line + "\n")

def write_raw_schema(slug: str, json_ld_data: List[Dict]):
    os.makedirs(RAW_SCHEMA_DIR, exist_ok=True)
    json_path = os.path.join(RAW_SCHEMA_DIR, f"{slug}.json")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(json_ld_data, jf, indent=2, ensure_ascii=False)
