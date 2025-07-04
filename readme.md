# 📜 Structured Web Auditor
## An Open, Zero-Trust Framework for Verifiable, Semantic, and Provenance-Based Site Auditing

---

## 📌 Abstract

The **Structured Web Auditor** is an open-source, zero-trust auditing tool designed to verify the integrity, alignment, and provenance of any web node participating in the emerging **AI Structured Web** ecosystem.

Built to be **auditable by design**, this tool enforces strict criteria for site performance, zero-trust principles (no unwanted cookies, no autoloaded popups/scripts), backlink verification for trust mesh participation, and semantic alignment between structured data (JSON-LD, microdata) and visible HTML.

This whitepaper documents its purpose, mechanics, and deployment, presenting it as a reproducible standard for modern, transparent web verification — a thesis on proving trust, sustainability, and alignment in an age where content provenance matters as much as raw ranking.

---

## 🔑 Purpose

The Structured Web Auditor exists for one reason:  
**To verify that any web node claims what it says it claims — and proves it through frictionless, machine-readable alignment.**

At its core, the Auditor validates:

✅ **Site speed & performance:** Fast pages prove operational efficiency.  
✅ **Zero-Trust enforcement:** No hidden cookies, no stealth popups, no unauthorized scripts.  
✅ **Structured Data presence:** JSON-LD and microdata must exist and match.  
✅ **Semantic alignment:** The actual human-visible content must reflect what the structured data says.  
✅ **Trust mesh participation:** Mandatory backlink to a canonical verification URL ensures nodes are connected and transparent.

**The end goal is simple:**  
> **Trust is proven. Not assumed.**

---

## ⚙️ How It Works

The tool operates in three modes:

### 1️⃣ Single URL Audit  
Manually verify any single page’s integrity. Useful for spot-checks and testing drafts.

### 2️⃣ Full Sitemap Audit  
Parse an entire domain’s `sitemap.xml`. The auditor crawls every listed URL and produces detailed page reports plus a domain rollup.

### 3️⃣ Mesh-Wide Audit  
For nodes participating in a structured trust mesh, the Auditor auto-loads `mesh.json`, discovers all nodes, auto-resolves their `sitemap.xml`, and recursively verifies every page.

---

## 🔍 Core Checks

Each page undergoes **5 integrated modules**:

### 1. Performance Audit  
- Measures actual page load time.  
- Flags the homepage if it exceeds the 1-second threshold (configurable).  
- Checks for excessive JS that auto-loads on non-home pages.

### 2. Schema Audit  
- Confirms valid JSON-LD presence.  
 - Parses microdata when available using `itemtype`/`itemprop` attributes.
- Validates JSON structure for `.json` endpoints.  
- Flags missing or invalid markup.

### 3. Trust Backlink Audit  
- Verifies the required backlink `isPartOf` or `sameAs` property in JSON-LD.  
- For `/verify.html`, also checks for visible `<a>` tags linking to the canonical `https://structuredweb.org/verify`.  
- Produces a scored trust mark from 0 to 4 points:  
  - `/` root (1)  
  - `/verify.html` (2: structured + visible)  
  - `/verify.json` (1)

### 4. Zero-Trust Audit  
- Crawls the DOM for popups and overlays.  
- Tests whether cookies are set server-side without explicit user interaction.  
- Whitelists trusted edge assets only.  
- Fails pages that violate the zero-trust standard.

### 5. Semantic Alignment Audit  
- Extracts keywords from visible text.  
- Compares to extracted descriptions and keyword arrays in JSON-LD & microdata.  
- Calculates a raw alignment score — % of structured keywords found in actual page content.
- Structured keywords now include both JSON-LD and microdata terms.
- Reports missing keywords to guide realignment.

---

## 🧮 Meta Scoring

Each page is scored:

- **100 points baseline**
- -25 if no structured data.
- -20 if required backlinks missing.
- -25 if zero-trust violations found.
- -10 for slow homepage.
- -10 scaled if semantic alignment is below 70%.
- -5 for general FAIL status (this means if any core module fails, you lose an extra 5 points — this ensures the worst possible page can’t score more than 5, never 0)

A final site report combines:

- Total pages checked.
- Pages passed vs failed.
- Average page score.
- Average semantic alignment.
- Overall mesh trust grade (Perfect, Good, Needs Work, Not Eligible).

---

## 📂 Outputs

- **Per-page text report:** Detailed breakdown of checks, found keywords, violations.  
- **Raw JSON-LD dump:** Each node’s structured data is archived for full transparency.  
- **Site report:** Single `.txt` summary rolls up all scores, backlink scores, semantic overlap, and key observations.

---

## 🚦 How to Run It

1️⃣ **Clone the repo** or drop the scripts in your project.  
2️⃣ Install dependencies:  

```bash
pip install requests beautifulsoup4
```

3️⃣ Run the main auditor:  

```bash
python audit.py
```

4️⃣ Choose mode:  

- `[1]` Single URL → `https://example.com/page`  
- `[2]` Full Sitemap → `example.com`  
- `[3]` Mesh → auto-loads `mesh.json` at `https://structuredweb.org/mesh.json`

5️⃣ Check `outputs/` for:  

- `outputs/pages` → Page-level text reports & JSON-LD snapshots.  
- `outputs/sites` → Combined site trust scorecards.

---

## 🕵️‍♂️ Why It Matters

Search engines and LLMs increasingly prioritize provenance, cohesion, and structured clarity.  
Any node passing this audit demonstrates:

- High provenance: Data & content align.  
- Verifiable trust: Links prove participation in a larger mesh.  
- Zero hidden traps: Cookies, popups, stealth scripts — all flagged.  
- Alignment for inferencing: Semantic overlap means agents can trust what they read.

This is a modern testbed for frictionless trust.  
No hidden crawl tricks. No cookie bait.  
Just transparent, machine-verifiable trust — auditable by anyone, anytime.

---

## 🧬 The Thesis

> **A frictionless, open, structured web can maintain trust and relevance far longer than opaque, ever-shifting algorithmic ranking alone.**

This bot operationalizes that thesis:

- By quantifying trust.  
- By rewarding alignment.  
- By rejecting dark patterns.  
- By recording transparent provenance forever.

---

## 💡 Closing

Deploy it. Fork it. Extend it.  
This is the WordPress of verifiable provenance: Simple enough to adopt, strict enough to hold the line.

**Learn more → [structuredweb.org/verify](https://structuredweb.org/verify)**  
**Audit your site → `/mesh.json`**  
**Stay zero-trust, always.**
