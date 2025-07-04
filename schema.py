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

    # Extract microdata using itemtype and itemprop attributes
    micro_items = []
    for scope in soup.select("[itemscope]"):
        item = {
            "type": scope.get("itemtype", ""),
            "props": {},
            "html": str(scope)
        }
        for prop in scope.find_all(attrs={"itemprop": True}, recursive=False):
            key = prop.get("itemprop")
            val = prop.get("content") or prop.get_text(strip=True)
            item["props"][key] = val
        if item["props"]:
            micro_items.append(item)

    result["has_microdata"] = bool(micro_items)
    result["microdata_data"] = micro_items

    if not json_ld and not micro_items:
        result["status"] = "FAIL"
        result["violations"].append("No structured data found.")

    return result
