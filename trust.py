from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

REQUIRED_BACKLINK_URL = "https://structuredweb.org/verify"
REQUIRED_PATHS = {"/", "/verify.html", "/verify.json", "/verify"}

def find_backlink_in_json(obj) -> bool:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == "ispartof" and isinstance(v, dict):
                if v.get("url", "").strip().lower() == REQUIRED_BACKLINK_URL:
                    return True
            if k.lower() == "sameas":
                if isinstance(v, list):
                    if REQUIRED_BACKLINK_URL in [str(item).strip().lower() for item in v]:
                        return True
            if isinstance(v, (dict, list)):
                if find_backlink_in_json(v):
                    return True
            elif isinstance(v, str):
                if v.strip().lower() == REQUIRED_BACKLINK_URL:
                    return True
    elif isinstance(obj, list):
        for item in obj:
            if find_backlink_in_json(item):
                return True
    return False

def audit_backlink(url: str, html_content: str) -> dict:
    parsed = urlparse(url)
    path = (parsed.path or "/").rstrip("/") or "/"
    is_verify_html = path in ["/verify", "/verify.html"]
    is_verify_json = path == "/verify.json"
    is_home = path == "/"

    result = {
        "status": "PASS",
        "violations": [],
        "required": path in REQUIRED_PATHS,
        "backlink_found": False,
        "html_backlink": False,
        "sd_backlink": False,
        "backlink_score": None
    }

    found_json = False
    found_html = False

    if is_verify_json:
        try:
            data = json.loads(html_content)
            found_json = find_backlink_in_json(data)
        except json.JSONDecodeError:
            found_json = False
        result["sd_backlink"] = found_json
        if not found_json:
            result["status"] = "FAIL"
            result["violations"].append("Missing required isPartOf backlink in /verify.json structured data.")
    else:
        soup = BeautifulSoup(html_content, "html.parser")

        # Check JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if find_backlink_in_json(data):
                    found_json = True
                    break
            except json.JSONDecodeError:
                continue
        result["sd_backlink"] = found_json

        if path in REQUIRED_PATHS and not found_json:
            result["status"] = "FAIL"
            result["violations"].append(f"{path} is missing isPartOf backlink in structured data.")

        # Strict visible HTML anchor check
        if is_verify_html:
            for tag in soup.find_all("a", href=True):
                href = tag["href"].strip().lower()
                text = tag.get_text(strip=True).lower()
                if href == REQUIRED_BACKLINK_URL and "structuredweb.org/verify" in text:
                    found_html = True
                    break
            result["html_backlink"] = found_html
            if not found_html:
                result["status"] = "FAIL"
                result["violations"].append(f"{path} is missing visible HTML link to {REQUIRED_BACKLINK_URL}")

    # Score logic
    if path in REQUIRED_PATHS:
        score = 0
        if result["sd_backlink"]:
            score += 1
        if is_verify_html and result["html_backlink"]:
            score += 1
        result["backlink_score"] = score
    else:
        result["backlink_score"] = None

    result["backlink_found"] = result["sd_backlink"] or result["html_backlink"]

    # Verify.html must contain both
    if is_verify_html and (not result["sd_backlink"] or not result["html_backlink"]):
        result["status"] = "FAIL"
        result["violations"].append(f"{path} must contain both structured data and visible HTML backlink.")

    # Non-required routes skip backlink reporting
    if path not in REQUIRED_PATHS:
        result["violations"] = []

    return result
