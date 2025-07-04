# structuredweb_auditor/audit.py

import sys
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from core.audit_runner import audit_page
from core.site_report import write_combined_report

def resolve_url(raw: str) -> str:
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    parsed = urlparse(raw)
    if not parsed.netloc:
        raise ValueError("Invalid URL — missing domain.")
    return raw.rstrip("/") + "/" if parsed.path in ["", "/"] else raw

def parse_sitemap(sitemap_url: str) -> list:
    try:
        resp = requests.get(sitemap_url, timeout=10)
        soup = BeautifulSoup(resp.content, "xml")
        return [loc.text.strip() for loc in soup.find_all("loc")]
    except Exception as e:
        print(f"❌ Failed to load sitemap: {str(e)}")
        return []

def parse_mesh() -> list:
    mesh_url = "https://structuredweb.org/mesh.json"
    print(f"\n📡 Auto-loading mesh from: {mesh_url}")

    try:
        resp = requests.get(mesh_url, timeout=10)
        data = resp.json()
    except Exception as e:
        print(f"❌ Failed to fetch or parse mesh.json: {str(e)}")
        return []

    sitemaps = set()
    dist = data.get("distribution", [])
    if not isinstance(dist, list):
        print("⚠️ 'distribution' is missing or malformed.")
        return []

    for item in dist:
        content_url = item.get("contentUrl", "") if isinstance(item, dict) else ""
        if "/verify.json" in content_url:
            base_url = content_url.rsplit("/verify.json", 1)[0]
            sitemap_url = base_url + "/sitemap.xml"
            sitemaps.add(sitemap_url)

    return sorted(sitemaps)

def main():
    print("Welcome to Structured Web Auditor\n")
    print("What would you like to audit?")
    print("[1] Single URL")
    print("[2] Full sitemap of a domain")
    print("[3] Entire mesh (all pages in mesh.json sitemaps)\n")

    choice = input("Enter choice [1–3]: ").strip()

    if choice == "1":
        raw_url = input("Enter the full or partial URL to audit: ").strip()
        try:
            url = resolve_url(raw_url)
        except ValueError as ve:
            print(f"\n❌ {ve}")
            sys.exit(1)

        print(f"\n📡 Auditing {url}...\n")
        result = audit_page(url)
        print_summary(result)

    elif choice == "2":
        domain = input("Enter domain (e.g., example.com): ").strip().lower()
        sitemap_url = f"https://{domain}/sitemap.xml"

        print(f"\n📂 Fetching sitemap: {sitemap_url}")
        urls = parse_sitemap(sitemap_url)
        if not urls:
            print("⚠️ No URLs found in sitemap.")
            sys.exit(1)

        print(f"🔍 Found {len(urls)} URLs. Beginning audit...\n")
        page_reports = []
        for i, url in enumerate(urls):
            print(f"  [{i+1}/{len(urls)}] Auditing: {url}")
            result = audit_page(url)
            page_reports.append(result)

        write_combined_report(domain, page_reports)
        print("✅ Domain-wide audit complete.")

    elif choice == "3":
        sitemaps = parse_mesh()
        if not sitemaps:
            print("⚠️ No sitemaps found in mesh.")
            sys.exit(1)

        all_urls = []
        for sm in sitemaps:
            print(f"\n📂 Parsing sitemap: {sm}")
            urls = parse_sitemap(sm)
            if urls:
                all_urls.extend(urls)

        print(f"\n🔍 Total URLs found across mesh: {len(all_urls)}\n")
        page_reports = []
        for i, url in enumerate(all_urls):
            print(f"  [{i+1}/{len(all_urls)}] Auditing: {url}")
            result = audit_page(url)
            page_reports.append(result)

        write_combined_report("structuredweb.org", page_reports)
        print("✅ Mesh-wide audit complete.")

    else:
        print("Invalid choice.")
        sys.exit(1)

def print_summary(result: dict):
    print("=" * 60)
    print(f"🧾 Audit Complete: {result['url']}")
    print(f"Status: {result['status']}")
    print(f"Load time: {result.get('load_time_ms', 'n/a')} ms")
    print(f"Backlink required: {result.get('backlink_required', 'n/a')}")
    print(f"Backlink found: {result.get('backlink_found', 'n/a')}")
    print(f"Structured Data: {result.get('structured_data_present', False)}")
    print(f"Alignment Score: {result.get('alignment_percent', 0)}%")
    print("\nViolations:")
    if result.get("violations"):
        for v in result["violations"]:
            print(f" - {v}")
    else:
        print("None ✅")
    print("=" * 60)

if __name__ == "__main__":
    main()
