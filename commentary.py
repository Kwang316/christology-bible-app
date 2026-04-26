"""
Approved commentary sources manager.
Reads sources/manifest.json and searches commentary text files by keyword.
"""

import json
import os
import re

SOURCES_DIR = os.path.join(os.path.dirname(__file__), "sources")
MANIFEST_PATH = os.path.join(SOURCES_DIR, "manifest.json")


def load_manifest() -> list[dict]:
    """Load the approved sources manifest."""
    if not os.path.isfile(MANIFEST_PATH):
        return []
    try:
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return [s for s in data.get("sources", []) if s.get("approved", False)]
    except Exception:
        return []


def search_commentary(keywords: list[str], max_per_source: int = 3) -> list[dict]:
    """
    Search all approved commentary sources for passages mentioning any keyword.
    Returns a list of {author, title, year, excerpt} dicts.
    """
    sources = load_manifest()
    results: list[dict] = []

    for source in sources:
        file_path = os.path.join(SOURCES_DIR, source.get("file", ""))
        if not os.path.isfile(file_path):
            continue
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        paragraphs = [p.strip() for p in re.split(r'\n{2,}', content) if p.strip()]
        found = 0
        for para in paragraphs:
            if found >= max_per_source:
                break
            if any(re.search(r'\b' + re.escape(kw) + r'\b', para, re.IGNORECASE) for kw in keywords):
                results.append({
                    "author": source.get("author", "Unknown"),
                    "title": source.get("title", ""),
                    "year": source.get("year", ""),
                    "excerpt": para[:600] + ("…" if len(para) > 600 else ""),
                })
                found += 1

    return results


def list_approved_sources() -> list[dict]:
    """Return all approved sources with metadata (no content)."""
    return [
        {
            "author": s.get("author", ""),
            "title": s.get("title", ""),
            "year": s.get("year", ""),
            "description": s.get("description", ""),
            "file": s.get("file", ""),
        }
        for s in load_manifest()
    ]


def add_source_to_manifest(
    author: str,
    title: str,
    year: str | int,
    file_name: str,
    description: str = "",
    approved: bool = False,
) -> bool:
    """
    Register a new commentary source in manifest.json.
    Set approved=True to make it searchable immediately.
    """
    if not os.path.isfile(MANIFEST_PATH):
        data: dict = {"sources": []}
    else:
        try:
            with open(MANIFEST_PATH, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"sources": []}

    sources: list[dict] = data.get("sources", [])
    # Prevent duplicates by file name
    if any(s.get("file") == file_name for s in sources):
        return False

    sources.append({
        "author": author,
        "title": title,
        "year": year,
        "file": file_name,
        "description": description,
        "approved": approved,
    })
    data["sources"] = sources

    try:
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False
