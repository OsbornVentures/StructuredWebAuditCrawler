# structuredweb_auditor/rules/zero_trust.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

EDGE_WHITELIST = ["kworker", "durable", "do.cloudflare"]
USER_AGENT = "StructuredWebAuditor/1.0"

def audit_zero_trust(url: str, html_content: str) -> dict:
    debug_log = [f"🔍 Zero Trust Audit: {url}"]

    result = {
        "status": "PASS",
        "violations": [],
        "autoloaded_scripts": [],
        "blocked_cookies": [],
        "popup_detected": False,
        "debug_log": debug_log
    }

    parsed = urlparse(url)
    is_homepage = parsed.path in ["/", ""]

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Detect external scripts
    script_tags = soup.find_all("script", src=True)
    for tag in script_tags:
        src = tag["src"]
        if not any(allowed in src for allowed in EDGE_WHITELIST):
            result["autoloaded_scripts"].append(src)

    if result["autoloaded_scripts"]:
        msg = f"✘ Autoloaded scripts found: {result['autoloaded_scripts']}"
    else:
        msg = "✓ No disallowed autoloaded JS"
    print(msg)
    debug_log.append(msg)

    # 2. Check for cookies
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        if response.cookies:
            for cookie in response.cookies:
                cookie_str = f"{cookie.name}={cookie.value}"
                result["blocked_cookies"].append(cookie_str)
    except Exception as e:
        msg = f"⚠️ Cookie check failed: {e}"
        debug_log.append(msg)
        print(msg)

    if result["blocked_cookies"]:
        msg = f"✘ Cookies set without user action: {result['blocked_cookies']}"
    else:
        msg = "✓ No cookies set by server"
    print(msg)
    debug_log.append(msg)

    # 3. Look for overlays/popups
    overlays = soup.select("[class*='popup'], [id*='popup'], [class*='overlay'], [id*='overlay']")
    if overlays:
        result["popup_detected"] = True
        msg = "✘ Popup or overlay elements detected"
    else:
        msg = "✓ No popup or overlay detected"
    print(msg)
    debug_log.append(msg)

    # 4. Enforcement (non-homepage only)
    if not is_homepage:
        if result["autoloaded_scripts"]:
            result["status"] = "FAIL"
            result["violations"].append(f"Autoloaded JS on non-homepage: {result['autoloaded_scripts']}")

        if result["blocked_cookies"]:
            result["status"] = "FAIL"
            result["violations"].append("Cookies set without interaction")

        if result["popup_detected"]:
            result["status"] = "FAIL"
            result["violations"].append("Popup or overlay detected on load")

    status_msg = f"→ Page Status: {result['status']}"
    print(status_msg)
    debug_log.append(status_msg)

    return result
