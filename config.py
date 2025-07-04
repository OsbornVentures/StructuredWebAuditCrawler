# structuredweb_auditor/config.py

# Paths
OUTPUT_DIR = "outputs"
PAGES_DIR = f"{OUTPUT_DIR}/pages"
SITES_DIR = f"{OUTPUT_DIR}/sites"
RAW_SCHEMA_DIR = f"{PAGES_DIR}/raw_schema"

# User-Agent
USER_AGENT = "StructuredWebAuditor/1.0"

# Backlink enforcement
REQUIRED_BACKLINK_PATHS = ["/", "/verify.html", "/verify.json"]
TRUST_URL = "https://structuredweb.org/verify"

# Scoring thresholds
ALIGNMENT_THRESHOLD = 70  # percent
HOMEPAGE_MAX_LOAD_MS = 1000  # ms

# Audit Order (for future sitemap/mesh sorting)
AUDIT_ORDER = [
    "/robots.txt",
    "/ai.json", "/ai.html",
    "/verify.json",
    "/mesh.json",
    "/manifest.json",
    "/assistant_context.json",
    "/sitemap.xml",
    "/genesis.txt", "/humans.txt"  # bonus only
]
