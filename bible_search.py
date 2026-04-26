"""
Bible keyword search engine.
Searches local kjv_by_chapter.json for topic-related verses.
"""

import re
import json
import os

CANONICAL_ORDER = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
    "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
    "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
    "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
    "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation",
]

BOOK_ORDER = {book: i for i, book in enumerate(CANONICAL_ORDER)}

# Topic → KJV search keywords
TOPIC_KEYWORDS: dict[str, list[str]] = {
    "math": ["number", "count", "measure", "multiply", "sum", "numbered", "counted", "measured", "arithmetic", "calculation"],
    "mathematics": ["number", "count", "measure", "multiply", "numbered", "counted", "measured"],
    "numbers": ["number", "numbered", "count", "countless"],
    "love": ["love", "charity", "loveth", "lovest", "beloved", "lovingkindness"],
    "hate": ["hate", "hateth", "hated", "despise", "abhor"],
    "fear": ["fear", "afraid", "terror", "dread", "fearful", "feared"],
    "wisdom": ["wisdom", "wise", "understanding", "knowledge", "discernment", "prudent"],
    "prayer": ["pray", "prayer", "praying", "supplication", "intercede", "petition"],
    "faith": ["faith", "believe", "belief", "trust", "faithful"],
    "hope": ["hope", "hopeth", "expectation", "wait upon"],
    "money": ["money", "silver", "gold", "riches", "wealth", "mammon", "covet", "greed"],
    "sin": ["sin", "sinned", "transgression", "iniquity", "wickedness", "trespass"],
    "forgiveness": ["forgive", "forgiven", "pardon", "merciful", "mercy", "remission"],
    "salvation": ["salvation", "save", "saved", "redeem", "redeemed", "deliverance"],
    "heaven": ["heaven", "paradise", "eternal life", "glory", "kingdom of God"],
    "hell": ["hell", "gehenna", "fire", "destruction", "damnation"],
    "marriage": ["marriage", "married", "husband", "wife", "wed", "wedlock"],
    "children": ["children", "child", "son", "daughter", "offspring", "seed"],
    "work": ["work", "labor", "labour", "diligent", "slothful", "toil"],
    "truth": ["truth", "true", "honest", "faithful", "verity"],
    "peace": ["peace", "peaceable", "rest", "quiet", "tranquility"],
    "joy": ["joy", "rejoice", "rejoiceth", "glad", "delight", "happiness"],
    "anger": ["anger", "wrath", "furious", "rage", "indignation"],
    "humility": ["humble", "humility", "meek", "lowly", "modest"],
    "pride": ["pride", "proud", "haughty", "arrogant", "boast"],
    "death": ["death", "die", "died", "mortality", "perish"],
    "life": ["life", "live", "living", "breath", "soul"],
    "god": ["God", "LORD", "Almighty", "Creator", "Father"],
    "jesus": ["Jesus", "Christ", "Messiah", "Son of God", "Saviour", "Redeemer"],
    "holy spirit": ["Holy Spirit", "Holy Ghost", "Spirit of God", "Comforter"],
    "suffering": ["suffering", "affliction", "tribulation", "sorrow", "grief", "pain"],
    "healing": ["heal", "healed", "healing", "restore", "cure", "health"],
    "creation": ["created", "creation", "made the heavens", "beginning", "formed"],
    "light": ["light", "lamp", "shine", "luminous", "brightness"],
    "darkness": ["darkness", "dark", "shadow", "night"],
    "water": ["water", "rivers", "flood", "rain", "sea", "ocean"],
    "food": ["food", "bread", "eat", "feast", "hunger", "famine"],
    "leadership": ["leader", "ruler", "king", "authority", "govern", "shepherd"],
    "justice": ["justice", "righteous", "judgment", "equity", "fair"],
    "generosity": ["give", "generous", "charity", "tithe", "offering", "gift"],
    "patience": ["patient", "patience", "long-suffering", "endure", "persevere"],
    "courage": ["courage", "courageous", "bold", "strong", "valiant", "fearless"],
    "trust": ["trust", "rely", "depend", "confidence", "assurance"],
    "obedience": ["obey", "obedience", "commandment", "law", "statute", "follow"],
    "family": ["family", "father", "mother", "brother", "sister", "household"],
    "friendship": ["friend", "friendship", "companion", "fellowship", "neighbor"],
    "time": ["time", "season", "day", "hour", "appointed", "eternity"],
    "strength": ["strength", "strong", "might", "power", "force"],
}


def expand_query(topic: str) -> list[str]:
    """Map a topic string to KJV search keywords."""
    topic_lower = topic.lower().strip()
    for key, keywords in TOPIC_KEYWORDS.items():
        if key == topic_lower or topic_lower in key or key in topic_lower:
            return keywords
    # Fallback: use the significant words of the query itself
    stop = {"what", "does", "the", "bible", "say", "about", "is", "are", "in", "a", "an", "and", "or"}
    words = [w for w in re.split(r'\W+', topic_lower) if w and w not in stop and len(w) > 2]
    return words if words else [topic_lower]


def search_kjv(kjv_doc: dict, keywords: list[str], max_results: int = 60) -> list[dict]:
    """
    Search kjv_by_chapter.json for verses matching any keyword (word-boundary match).
    Returns results sorted in canonical Bible order.
    """
    patterns = [re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE) for kw in keywords]
    results: list[dict] = []

    for book_name, chapters in kjv_doc.items():
        if not isinstance(chapters, dict):
            continue
        for ch_str, verses in chapters.items():
            if not isinstance(verses, list):
                continue
            for verse_obj in verses:
                text = verse_obj.get("text", "")
                matched_kws = [kw for kw, p in zip(keywords, patterns) if p.search(text)]
                if matched_kws:
                    v_num = verse_obj.get("verse", 0)
                    results.append({
                        "book": book_name,
                        "chapter": int(ch_str),
                        "verse": v_num,
                        "text": text.strip(),
                        "reference": f"{book_name} {ch_str}:{v_num}",
                        "testament": "OT" if BOOK_ORDER.get(book_name, 0) < 39 else "NT",
                        "matched_keywords": matched_kws,
                    })

    results.sort(key=lambda r: (BOOK_ORDER.get(r["book"], 99), r["chapter"], r["verse"]))
    return results[:max_results]


def highlight_keywords(text: str, keywords: list[str]) -> str:
    """Wrap matched keywords with <mark> tags for display."""
    for kw in keywords:
        pattern = re.compile(r'\b(' + re.escape(kw) + r')\b', re.IGNORECASE)
        text = pattern.sub(r'<mark>\1</mark>', text)
    return text


def load_kjv(path: str) -> dict | None:
    """Load kjv_by_chapter.json from disk."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        return doc if isinstance(doc, dict) else None
    except Exception:
        return None
