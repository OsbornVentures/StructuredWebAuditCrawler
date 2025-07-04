# structuredweb_auditor/rules/performance.py

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

USER_AGENT = "StructuredWebAuditor/1.0"

def audit_performance(url: str, html_content: str) -> dict:
    result = {
        "load_time_ms": None,
        "status": "PASS",
        "violations": [],
        "autoloaded_js": [],
        "cookies_set": []
    }

    # 1. Measure load time
    try:
        headers = {"User-Agent": USER_AGENT}
        start = time.perf_counter()
        response = requests.get(url, headers=headers, timeout=10)
        end = time.perf_counter()
        result["load_time_ms"] = int((end - start) * 1000)
    except Exception as e:
        result["status"] = "FAIL"
        result["violations"].append(f"Page load error: {str(e)}")
        return result

    # Homepage speed rule
    parsed_url = urlparse(url)
    is_homepage = parsed_url.path in ["/", ""]

    if is_homepage and result["load_time_ms"] > 1000:
        result["status"] = "FAIL"
        result["violations"].append(f"Homepage load time exceeds 1 second: {result['load_time_ms']}ms")

    # 2. Parse HTML for JS includes
    soup = BeautifulSoup(html_content, "html.parser")
    script_tags = soup.find_all("script", src=True)
    for tag in script_tags:
        src = tag["src"]
        if not any(allowed in src for allowed in ["kworker", "durable", "edge"]):
            result["autoloaded_js"].append(src)

    if result["autoloaded_js"] and not is_homepage:
        result["status"] = "FAIL"
        result["violations"].append(f"Autoloaded JS found: {result['autoloaded_js']}")

    # 3. Check cookies
    jar = requests.cookies.RequestsCookieJar()
    try:
        resp = requests.get(url, headers=headers, cookies=jar)
        if resp.cookies:
            for c in resp.cookies:
                result["cookies_set"].append(f"{c.name}={c.value}")
    except:
        pass

    if result["cookies_set"] and not is_homepage:
        result["status"] = "FAIL"
        result["violations"].append("Autoloaded cookies set without user interaction")

    return result
