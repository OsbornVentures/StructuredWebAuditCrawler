# structuredweb_auditor/rules/semantic_alignment.py

import re
from bs4 import BeautifulSoup
from typing import List, Dict

# Common and domain-specific noise terms to skip
STOPWORDS = set([
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
    "has", "have", "had", "you", "your", "our", "but", "not", "any", "can",
    "more", "all", "its", "out", "get", "how", "use", "see", "now", "new",
    "we", "us", "they", "their", "them", "it", "on", "in", "by", "as", "an",
    "of", "a", "to", "is", "or", "be", "at", "via", "if",

    # AI Structured Web domain-specific noise
    "structured", "web", "ai", "indexer", "resolver", "node", "mesh",
    "verify", "dual", "layered", "handshake", "agent", "subnode", "compliance",
    "claim", "license", "category", "link", "endpoint", "semantic", "trust"
])


def extract_keywords(text: str) -> List[str]:
    words = re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower())
    return [word for word in words if word not in STOPWORDS]


def extract_json_ld_keywords(json_ld_blocks: List[dict]) -> List[str]:
    descriptions = []

    def extract_desc(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if "description" in k.lower() or "keywords" in k.lower():
                    if isinstance(v, str):
                        descriptions.append(v)
                    elif isinstance(v, list):
                        descriptions.extend([str(i) for i in v])
                elif isinstance(v, (dict, list)):
                    extract_desc(v)
        elif isinstance(obj, list):
            for item in obj:
                extract_desc(item)

    for block in json_ld_blocks:
        extract_desc(block)

    return extract_keywords(" ".join(descriptions))


def extract_microdata_keywords(microdata_items: List[dict]) -> List[str]:
    desc_texts = []
    for item in microdata_items:
        props = item.get("props", {})
        for key, val in props.items():
            if "description" in key.lower() and isinstance(val, str):
                desc_texts.append(val)
    return extract_keywords(" ".join(desc_texts))


def audit_semantic_alignment(
    html: str,
    json_ld_blocks: List[dict],
    microdata_items: List[dict]
) -> Dict:
    soup = BeautifulSoup(html, "html.parser")
    html_text = soup.get_text(separator=" ", strip=True)
    html_keywords = set(extract_keywords(html_text))

    json_keywords = set(extract_json_ld_keywords(json_ld_blocks))
    micro_keywords = set(extract_microdata_keywords(microdata_items))

    shared = json_keywords.intersection(html_keywords)
    all_keywords = json_keywords.union(html_keywords)

    alignment_percent = (
        round(len(shared) / len(json_keywords) * 100, 2) if json_keywords else 0
    )

    return {
        "alignment_percent": alignment_percent,
        "shared_terms": sorted(list(shared)),
        "missing_terms": sorted(list(json_keywords - html_keywords)),
        "total_sd_terms": len(json_keywords)
    }
