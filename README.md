# 📜 Structured Web Auditor

## An Open, Zero-Trust Framework for Verifiable, Semantic, and Provenance-Based Site Auditing

---

### 📌 Abstract

The Structured Web Auditor is an open-source, zero-trust auditing tool designed to verify the integrity, alignment, and provenance of any web node participating in the emerging AI Structured Web ecosystem.

Built to be auditable by design, this tool enforces strict criteria for site performance, zero-trust principles (no unwanted cookies, no autoloaded popups/scripts), backlink verification for trust mesh participation, and semantic alignment between structured data (JSON-LD, microdata) and visible HTML.

This whitepaper documents its purpose, mechanics, and deployment, presenting it as a reproducible standard for modern, transparent web verification — a thesis on proving trust, sustainability, and alignment in an age where content provenance matters as much as raw ranking.

---

### 🔑 Purpose

The Structured Web Auditor exists for one reason:  
**To verify that any web node claims what it says it claims — and proves it through frictionless, machine-readable alignment.**

At its core, the Auditor validates:

- ✅ **Site speed & performance:** Fast pages prove operational efficiency.
- ✅ **Zero-Trust enforcement:** No hidden cookies, no stealth popups, no unauthorized scripts.
- ✅ **Structured Data presence:** JSON-LD and microdata must exist and match.
- ✅ **Semantic alignment:** The actual human-visible content must reflect what the structured data says.
- ✅ **Trust mesh participation:** Mandatory backlink to a canonical verification URL ensures nodes are connected and transparent.

**The end goal is simple:**  
Trust is proven. Not assumed.

---

### ⚙️ How It Works

The tool operates in three modes:

1. **Single URL Audit**  
   Manually verify any single page’s integrity. Useful for spot-checks and testing drafts.

2. **Full Sitemap Audit**  
   Parse an entire domain’s `sitemap.xml`. The auditor crawls every listed URL and produces detailed page reports plus a domain rollup.

3. **Mesh-Wide Audit**  
   For nodes participating in a structured trust mesh, the Auditor auto-loads `mesh.json`, discovers all nodes, auto-resolves their `sitemap.xml`, and recursively verifies every page.

---

### 🔍 Core Checks

Each page undergoes 5 integrated modules:

1. **Performance Audit**
   - Measures actual page load time.
   - Flags the homepage if it exceeds the 1-second threshold (configurable).
   - Checks for excessive JS that auto-loads on non-home pages.

2. **Schema Audit**
   - Confirms valid JSON-LD presence.
   - Parses microdata when available.
   - Validates JSON structure for `.json` endpoints.
   - Flags missing or invalid markup.

3. **Trust Backlink Audit**
   - Verifies the required backlink `isPartOf` or `sameAs` property in JSON-LD.
   - For `/verify.html`, also checks for visible `<a>` tags linking to the canonical `https://structuredweb.org/verify`.
   - Produces a scored trust mark from 0 to 4 points:
     - `/` root (1)
     - `/verify.html` (2: structured + visible)
     - `/verify.json` (1)

4. **Zero-Trust Audit**
   - Crawls the DOM for popups and overlays.
   - Tests whether cookies are set server-side without explicit user interaction.
   - Whitelists trusted edge assets only.
   - Fails pages that violate the zero-trust standard.

5. **Semantic Alignment Audit**
   - Extracts keywords from visible text.
   - Compares to extracted descriptions and keyword arrays in JSON-LD & microdata.
   - Calculates a raw alignment score — % of structured keywords found in actual page content.
   - Reports missing keywords to guide realignment.

---

### 🧮 Meta Scoring

Each page is scored:

- 100 points baseline.
- -25 if no structured data.
- -20 if required backlinks missing.
- -25 if zero-trust violations found.
- -10 for slow homepage.
- -10 scaled if semantic alignment below 70%.
- -5 for general FAIL status.

A final site report combines:

- Total pages checked.
- Pages passed vs failed.
- Average page score.
- Average semantic alignment.
- Overall mesh trust grade (Perfect, Good, Needs Work, Not Eligible).

---

### 📂 Outputs

- **Per-page text report:** Detailed breakdown of checks, found keywords, violations.
- **Raw JSON-LD dump:** Each node’s structured data is archived for full transparency.
- **Site report:** Single `.txt` summary rolls up all scores, backlink scores, semantic overlap, and key observations.

---

### 🚦 How to Run It

1. Clone the repo or drop the scripts in your project.
2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
