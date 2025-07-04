from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json

def audit_schema(url: str, html_content: str) -> dict:
    result = {
        "status": "PASS",
        "violations": [],
        "has_json_ld": False,
        "has_microdata": False,
        "json_ld_data": [],
        "microdata_data": [],
    }

    parsed = urlparse(url)
    path = parsed.path.lower()

    if path.endswith(".json"):
        try:
            parsed_json = json.loads(html_content)
            if isinstance(parsed_json, dict):
                result["json_ld_data"] = [parsed_json]
                result["has_json_ld"] = True
            elif isinstance(parsed_json, list):
                result["json_ld_data"] = parsed_json
                result["has_json_ld"] = True
            else:
                result["status"] = "FAIL"
                result["violations"].append("Unsupported JSON structure.")
        except json.JSONDecodeError:
            result["status"] = "FAIL"
            result["violations"].append("Invalid JSON.")
        return result

    # Regular HTML structured data logic
    soup = BeautifulSoup(html_content, "html.parser")
    json_ld = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, dict):
                json_ld.append(data)
            elif isinstance(data, list):
                json_ld.extend(data)
        except json.JSONDecodeError:
            continue

    result["has_json_ld"] = bool(json_ld)
    result["json_ld_data"] = json_ld

    if not json_ld:
        result["status"] = "FAIL"
        result["violations"].append("No JSON-LD structured data found.")

    return result
