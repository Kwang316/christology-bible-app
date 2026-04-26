"""
Bible Zettelkasten — Brain-Connection App
GVCC Reading Schedule × Cytoscape.js Graph × KJV Bible Reader
"""

import streamlit as st
import streamlit.components.v1 as components
import html as html_module
import json
import os
import re
import csv
import time
import requests
from datetime import date, datetime
from urllib.parse import quote, unquote
import schedule_data as sched

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS · Scripture Graph",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="◈",
)

# ─────────────────────────────────────────────────────────────
# UI THEME — modern tech / HUD (mesh + glass + mono accents)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Sora:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">

<style>
:root {
  --bg-deep:    #05080d;
  --bg-mid:     #0a1018;
  --surface:    rgba(12, 18, 28, 0.65);
  --glass:      rgba(18, 28, 42, 0.55);
  --card:       rgba(14, 22, 36, 0.85);
  --border:     rgba(56, 189, 248, 0.12);
  --border-hi:  rgba(34, 211, 238, 0.35);
  --cyan:       #22d3ee;
  --cyan-dim:   rgba(34, 211, 238, 0.15);
  --violet:     #a78bfa;
  --violet-dim: rgba(167, 139, 250, 0.12);
  --magenta:    #e879f9;
  --lime:       #bef264;
  --ot:         #fbbf24;
  --nt:         #38bdf8;
  --psm:        #4ade80;
  --text:       #e8eef7;
  --text-dim:   #8b9cb3;
  --text-faint: #5c6d82;
  --glow-cyan:  0 0 24px rgba(34, 211, 238, 0.12);
  --glow-violet: 0 0 28px rgba(167, 139, 250, 0.15);
  --radius:     14px;
  --radius-sm:  10px;
  --font-ui:    'Sora', system-ui, sans-serif;
  --font-mono:  'JetBrains Mono', ui-monospace, monospace;
  --font-read:  'Source Serif 4', Georgia, serif;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: var(--bg-deep) !important;
  color: var(--text) !important;
  font-family: var(--font-ui) !important;
}

.stApp::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background:
    radial-gradient(ellipse 120% 80% at 10% -20%, rgba(34, 211, 238, 0.08), transparent 50%),
    radial-gradient(ellipse 80% 60% at 100% 0%, rgba(167, 139, 250, 0.09), transparent 45%),
    radial-gradient(ellipse 60% 40% at 50% 100%, rgba(232, 121, 249, 0.05), transparent 50%),
    linear-gradient(180deg, var(--bg-deep) 0%, var(--bg-mid) 100%);
}

.stApp::after {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  opacity: 0.35;
  background-image:
    linear-gradient(rgba(34, 211, 238, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34, 211, 238, 0.03) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 90% 70% at 50% 40%, black, transparent);
}

.block-container, [data-testid="stAppViewContainer"] > div {
  position: relative;
  z-index: 1;
}

#MainMenu, footer, header { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.block-container {
  padding: 1rem 1.5rem 2rem !important;
  max-width: 100% !important;
}

/* ── Header HUD ─────────────────────────────────────────────── */
.app-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem 1rem;
  padding: 0.85rem 1.1rem;
  margin-bottom: 1.1rem;
  background: var(--glass);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--glow-cyan), inset 0 1px 0 rgba(255,255,255,0.04);
}
.app-header-brand {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  margin-right: 0.5rem;
}
.app-header h1 {
  font-family: var(--font-ui);
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0;
  background: linear-gradient(105deg, var(--cyan) 0%, var(--violet) 55%, var(--magenta) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.app-header-tagline {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--text-faint);
}
.app-header .date-pill,
.app-header .active-pill,
.app-header .stat-pill {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-dim);
}
.app-header .active-pill {
  border-color: rgba(167, 139, 250, 0.4);
  color: var(--violet);
  background: var(--violet-dim);
  box-shadow: var(--glow-violet);
}
.app-header .stat-pill {
  margin-left: auto;
  color: var(--cyan);
  border-color: rgba(34, 211, 238, 0.25);
  background: var(--cyan-dim);
}

.graph-focus-link {
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.06em;
  text-decoration: none !important;
  color: var(--cyan) !important;
  padding: 0.38rem 0.85rem !important;
  border-radius: 999px !important;
  border: 1px solid rgba(34, 211, 238, 0.35) !important;
  background: var(--cyan-dim) !important;
  align-self: center;
  white-space: nowrap;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.graph-focus-link:hover {
  box-shadow: var(--glow-cyan);
  border-color: var(--cyan) !important;
}

/* ── View mode bar (st.container border) ─────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--glass) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--glow-cyan), inset 0 1px 0 rgba(255,255,255,0.03);
  padding: 0.45rem 0.75rem !important;
  margin-bottom: 1rem !important;
}
.view-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-faint);
  display: inline-block;
  line-height: 2.2;
}

/* ── Panel titles ──────────────────────────────────────────── */
.panel-title {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--cyan);
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
  text-shadow: 0 0 20px rgba(34, 211, 238, 0.2);
}

/* ── Bible reader ──────────────────────────────────────────── */
.bible-text {
  font-family: var(--font-read);
  font-size: 1.42rem;
  line-height: 1.82;
  color: rgba(232, 238, 247, 0.94);
}
@media (max-width: 1100px) {
  .bible-text { font-size: 1.22rem; }
}
.verse-num {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--cyan);
  vertical-align: super;
  margin-right: 0.25rem;
  opacity: 0.9;
}
.active-verse-highlight {
  background: linear-gradient(90deg, rgba(34, 211, 238, 0.12), transparent);
  border-left: 3px solid var(--cyan);
  padding-left: 0.65rem;
  border-radius: 0 8px 8px 0;
  box-shadow: inset 0 0 24px rgba(34, 211, 238, 0.04);
}

/* ── Schedule pills ────────────────────────────────────────── */
.sched-pill {
  display: inline-block;
  border-radius: 8px;
  padding: 0.28rem 0.6rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 500;
  margin: 0.2rem 0.15rem;
  border: 1px solid transparent;
}
.pill-ot  { background: rgba(251, 191, 36, 0.18); color: #fde68a; border-color: rgba(251, 191, 36, 0.5); font-weight: 500; }
.pill-nt  { background: rgba(56, 189, 248, 0.18); color: #7dd3fc; border-color: rgba(56, 189, 248, 0.5); font-weight: 500; }
.pill-psm { background: rgba(74, 222, 128, 0.18); color: #86efac; border-color: rgba(74, 222, 128, 0.5); font-weight: 500; }

/* ── Inputs ────────────────────────────────────────────────── */
.stSelectbox label, .stNumberInput label, .stTextInput label, .stRadio label {
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  color: var(--text-dim) !important;
}
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.82rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--border-hi) !important;
  box-shadow: 0 0 0 1px rgba(34, 211, 238, 0.2) !important;
}

/* ── Buttons ───────────────────────────────────────────────── */
.stButton > button {
  font-family: var(--font-mono) !important;
  font-size: 0.76rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.04em !important;
  border-radius: var(--radius-sm) !important;
  border: 1px solid rgba(34, 211, 238, 0.35) !important;
  background: linear-gradient(165deg, rgba(34, 211, 238, 0.18), rgba(167, 139, 250, 0.12)) !important;
  color: var(--text) !important;
  padding: 0.45rem 1rem !important;
  transition: transform 0.15s, box-shadow 0.2s, border-color 0.2s !important;
}
.stButton > button:hover {
  border-color: var(--cyan) !important;
  box-shadow: var(--glow-cyan) !important;
  transform: translateY(-1px);
}
.stButton > button:active {
  transform: translateY(0);
}
.stButton.secondary > button {
  background: rgba(24, 32, 48, 0.85) !important;
  border-color: rgba(167, 139, 250, 0.42) !important;
  color: #ddd6fe !important;
}
.stButton.secondary > button:hover {
  border-color: var(--violet) !important;
  color: #f5f3ff !important;
  box-shadow: var(--glow-violet) !important;
}

/* ── Radio (view mode) ─────────────────────────────────────── */
div[data-testid="stRadio"] > div {
  gap: 0.35rem !important;
  flex-wrap: wrap !important;
}
div[data-testid="stRadio"] label {
  font-family: var(--font-mono) !important;
  font-size: 0.72rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.06em !important;
  padding: 0.35rem 0.65rem !important;
  border-radius: 999px !important;
  border: 1px solid transparent !important;
  background: transparent !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
  background: var(--cyan-dim) !important;
  border-color: rgba(34, 211, 238, 0.45) !important;
  color: var(--cyan) !important;
}

/* ── Expanders ─────────────────────────────────────────────── */
.streamlit-expanderHeader {
  font-family: var(--font-mono) !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.06em !important;
  background: var(--glass) !important;
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
}

/* ── Markdown & captions ───────────────────────────────────── */
label, .stMarkdown p, .stMarkdown li { color: var(--text) !important; }
.stCaption, [data-testid="stCaptionContainer"] {
  font-family: var(--font-mono) !important;
  font-size: 0.72rem !important;
  color: var(--text-dim) !important;
}
.stMarkdown h3 { color: var(--cyan) !important; font-family: var(--font-ui) !important; }

hr { border-color: var(--border) !important; opacity: 1; }

/* ── Scrollbar ─────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(34,211,238,0.35), rgba(167,139,250,0.35));
  border-radius: 6px;
}

/* ── Node info ─────────────────────────────────────────────── */
.node-info {
  font-family: var(--font-ui);
  background: var(--glass);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(167, 139, 250, 0.25);
  border-radius: var(--radius-sm);
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  font-size: 0.82rem;
  box-shadow: var(--glow-violet);
}
.node-info span {
  font-family: var(--font-mono);
  color: var(--violet);
  font-weight: 600;
}

/* ── Alerts ────────────────────────────────────────────────── */
.stSuccess, .stInfo, .stWarning, div[data-testid="stNotification"] {
  font-family: var(--font-mono) !important;
  font-size: 0.78rem !important;
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
  background: var(--card) !important;
}

/* ── Sidebar ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--bg-mid), var(--bg-deep)) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown h3 {
  font-family: var(--font-ui) !important;
  font-size: 1rem !important;
  background: linear-gradient(90deg, var(--cyan), var(--violet));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

[data-testid="column"] { min-height: 0; }

/* Split panes: height + overflow set inline by JS (data-nexus-split-pane) */
[data-nexus-split-pane="1"] {
  box-sizing: border-box !important;
  scrollbar-gutter: stable;
  padding-right: 0.35rem !important;
}
/* Inner grids inside a pane scroll with the parent, not their own viewport */
[data-nexus-split-pane="1"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
  max-height: none !important;
  height: auto !important;
  overflow: visible !important;
}

#brain-graph-anchor { scroll-margin-top: 1rem; }
.graph-inspector-anchor { scroll-margin-top: 5.5rem; }
.verse-click-hint {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-dim);
  margin: 0.4rem 0 0.6rem;
  padding: 0.5rem 0.65rem;
  border-left: 2px solid rgba(34, 211, 238, 0.4);
  background: rgba(34, 211, 238, 0.04);
  border-radius: 0 8px 8px 0;
}
.tsk-inline-row {
  margin-top: 0.85rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
}
.tsk-chip {
  display: inline-block;
  margin: 0.15rem 0.25rem 0.15rem 0;
  font-family: var(--font-mono);
  font-size: 0.65rem;
  padding: 0.22rem 0.5rem;
  border-radius: 8px;
  border: 1px solid rgba(167, 139, 250, 0.35);
  background: var(--violet-dim);
  color: var(--violet);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
CONNECTIONS_FILE = os.path.join(os.path.dirname(__file__), "connections.json")
GRAPH_META_FILE = os.path.join(os.path.dirname(__file__), "graph_meta.json")
GRAPH_ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "graph_archive")
VERSE_NOTES_FILE = os.path.join(os.path.dirname(__file__), "verse_notes.json")
EDGE_NOTES_FILE = os.path.join(os.path.dirname(__file__), "edge_notes.json")
MEMORIZATION_FILE = os.path.join(os.path.dirname(__file__), "verse_memorization.json")
DAILY_BRAIN_DIR = os.path.join(os.path.dirname(__file__), "brain_by_day")
API_BASE = "https://bible-api.com"
# Normalized local KJV (see download button in sidebar). Public-domain text via thiagobodruk/bible JSON.
KJV_LOCAL_FILE = os.path.join(os.path.dirname(__file__), "kjv_by_chapter.json")
KJV_SOURCE_JSON_URL = (
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"
)
GRAPH_INSPECTOR_PICK_PLACEHOLDER = "— choose verse —"
TSK_EDGES_FILE_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "normalized_edges.csv"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "normalized_edges.csv"),
]

BOOKS_OT = [
    "Genesis","Exodus","Leviticus","Numbers","Deuteronomy",
    "Joshua","Judges","Ruth","1 Samuel","2 Samuel",
    "1 Kings","2 Kings","1 Chronicles","2 Chronicles",
    "Ezra","Nehemiah","Esther","Job","Psalms","Proverbs",
    "Ecclesiastes","Song of Solomon","Isaiah","Jeremiah",
    "Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos",
    "Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah",
    "Haggai","Zechariah","Malachi",
]
BOOKS_NT = [
    "Matthew","Mark","Luke","John","Acts","Romans",
    "1 Corinthians","2 Corinthians","Galatians","Ephesians",
    "Philippians","Colossians","1 Thessalonians","2 Thessalonians",
    "1 Timothy","2 Timothy","Titus","Philemon","Hebrews",
    "James","1 Peter","2 Peter","1 John","2 John","3 John",
    "Jude","Revelation",
]
ALL_BOOKS = BOOKS_OT + BOOKS_NT
CHAPTERS_PER_BOOK = {
    "Genesis":50,"Exodus":40,"Leviticus":27,"Numbers":36,"Deuteronomy":34,
    "Joshua":24,"Judges":21,"Ruth":4,"1 Samuel":31,"2 Samuel":24,
    "1 Kings":22,"2 Kings":25,"1 Chronicles":29,"2 Chronicles":36,
    "Ezra":10,"Nehemiah":13,"Esther":10,"Job":42,"Psalms":150,
    "Proverbs":31,"Ecclesiastes":12,"Song of Solomon":8,"Isaiah":66,
    "Jeremiah":52,"Lamentations":5,"Ezekiel":48,"Daniel":12,"Hosea":14,
    "Joel":3,"Amos":9,"Obadiah":1,"Jonah":4,"Micah":7,"Nahum":3,
    "Habakkuk":3,"Zephaniah":3,"Haggai":2,"Zechariah":14,"Malachi":4,
    "Matthew":28,"Mark":16,"Luke":24,"John":21,"Acts":28,"Romans":16,
    "1 Corinthians":16,"2 Corinthians":13,"Galatians":6,"Ephesians":6,
    "Philippians":4,"Colossians":4,"1 Thessalonians":5,"2 Thessalonians":3,
    "1 Timothy":6,"2 Timothy":4,"Titus":3,"Philemon":1,"Hebrews":13,
    "James":5,"1 Peter":5,"2 Peter":3,"1 John":5,"2 John":1,"3 John":1,
    "Jude":1,"Revelation":22,
}

# TSK / normalized_edges.csv uses OSIS-style abbreviations (e.g. Gen.1.1, John.3.16)
BOOK_TO_TSK = {
    "Genesis": "Gen", "Exodus": "Exod", "Leviticus": "Lev", "Numbers": "Num",
    "Deuteronomy": "Deut", "Joshua": "Josh", "Judges": "Judg", "Ruth": "Ruth",
    "1 Samuel": "1Sam", "2 Samuel": "2Sam", "1 Kings": "1Kgs", "2 Kings": "2Kgs",
    "1 Chronicles": "1Chr", "2 Chronicles": "2Chr", "Ezra": "Ezra",
    "Nehemiah": "Neh", "Esther": "Esth", "Job": "Job", "Psalms": "Ps",
    "Proverbs": "Prov", "Ecclesiastes": "Eccl", "Song of Solomon": "Song",
    "Isaiah": "Isa", "Jeremiah": "Jer", "Lamentations": "Lam", "Ezekiel": "Ezek",
    "Daniel": "Dan", "Hosea": "Hos", "Joel": "Joel", "Amos": "Amos",
    "Obadiah": "Obad", "Jonah": "Jonah", "Micah": "Mic", "Nahum": "Nah",
    "Habakkuk": "Hab", "Zephaniah": "Zeph", "Haggai": "Hag", "Zechariah": "Zech",
    "Malachi": "Mal", "Matthew": "Matt", "Mark": "Mark", "Luke": "Luke",
    "John": "John", "Acts": "Acts", "Romans": "Rom", "1 Corinthians": "1Cor",
    "2 Corinthians": "2Cor", "Galatians": "Gal", "Ephesians": "Eph",
    "Philippians": "Phil", "Colossians": "Col", "1 Thessalonians": "1Thess",
    "2 Thessalonians": "2Thess", "1 Timothy": "1Tim", "2 Timothy": "2Tim",
    "Titus": "Titus", "Philemon": "Phlm", "Hebrews": "Heb", "James": "Jas",
    "1 Peter": "1Pet", "2 Peter": "2Pet", "1 John": "1John", "2 John": "2John",
    "3 John": "3John", "Jude": "Jude", "Revelation": "Rev",
}
TSK_TO_BOOK = {v: k for k, v in BOOK_TO_TSK.items()}


def display_ref_to_tsk_id(ref: str) -> str | None:
    """Convert 'John 3:16' or 'Genesis 1:1' to TSK id 'John.3.16', 'Gen.1.1'."""
    m = re.match(r"^(.+?)\s+(\d+):(\d+)$", ref.strip())
    if not m:
        return None
    book, ch, vs = m.group(1).strip(), m.group(2), m.group(3)
    abbr = BOOK_TO_TSK.get(book)
    if not abbr:
        return None
    return f"{abbr}.{ch}.{vs}"


def tsk_id_to_display_ref(tsk_id: str) -> str | None:
    """Convert 'Gen.1.1' to 'Genesis 1:1' for bible-api.com."""
    parts = tsk_id.strip().split(".")
    if len(parts) < 3:
        return None
    verse = parts[-1]
    chapter = parts[-2]
    book_abbr = ".".join(parts[:-2])
    book = TSK_TO_BOOK.get(book_abbr)
    if not book:
        return None
    return f"{book} {chapter}:{verse}"


# ─────────────────────────────────────────────────────────────
# PERSISTENCE
# ─────────────────────────────────────────────────────────────
def load_connections() -> dict:
    if os.path.exists(CONNECTIONS_FILE):
        try:
            with open(CONNECTIONS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"nodes": [], "edges": []}


def save_connections(data: dict):
    with open(CONNECTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_graph_meta() -> dict:
    if os.path.exists(GRAPH_META_FILE):
        try:
            with open(GRAPH_META_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_graph_meta(meta: dict) -> None:
    with open(GRAPH_META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def _split_right_panel_from_meta() -> str:
    s = load_graph_meta().get("split_right_panel", "graph")
    return s if s in ("graph", "inspector") else "graph"


def _persist_split_right_panel_to_meta() -> None:
    m = load_graph_meta()
    s = st.session_state.get("split_right_panel", "graph")
    m["split_right_panel"] = s if s in ("graph", "inspector") else "graph"
    save_graph_meta(m)


def maybe_daily_graph_rollover() -> None:
    """First run each calendar day: archive prior graph JSON, clear graph on disk + session."""
    today_s = date.today().isoformat()
    meta = load_graph_meta()
    stored = meta.get("graph_day")
    if stored == today_s:
        return
    if stored is not None:
        conn = load_connections()
        os.makedirs(GRAPH_ARCHIVE_DIR, exist_ok=True)
        if conn.get("nodes") or conn.get("edges"):
            arc = os.path.join(GRAPH_ARCHIVE_DIR, f"graph_{stored}.json")
            try:
                with open(arc, "w", encoding="utf-8") as f:
                    json.dump(conn, f, indent=2)
            except Exception:
                pass
        save_connections({"nodes": [], "edges": []})
        if "nodes" in st.session_state:
            st.session_state.nodes = []
        if "edges" in st.session_state:
            st.session_state.edges = []
        st.session_state.active_verse = None
        st.session_state._graph_rollover_notice = (
            f"New day — graph reset. Session **{stored}** archived as `graph_archive/graph_{stored}.json`. "
            "Use **PNG / PDF** on the graph toolbar before midnight if you want a snapshot too."
        )
    meta["graph_day"] = today_s
    save_graph_meta(meta)


def _json_file_mtime(path: str) -> float:
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


@st.cache_data(show_spinner=False)
def _load_verse_notes_cached(_mtime: float) -> dict:
    if not os.path.exists(VERSE_NOTES_FILE):
        return {}
    try:
        with open(VERSE_NOTES_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_verse_notes() -> dict:
    return _load_verse_notes_cached(_json_file_mtime(VERSE_NOTES_FILE))


def save_verse_notes(data: dict) -> None:
    with open(VERSE_NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@st.cache_data(show_spinner=False)
def _load_edge_notes_cached(_mtime: float) -> dict:
    if not os.path.exists(EDGE_NOTES_FILE):
        return {}
    try:
        with open(EDGE_NOTES_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_edge_notes() -> dict:
    return _load_edge_notes_cached(_json_file_mtime(EDGE_NOTES_FILE))


def save_edge_notes(data: dict) -> None:
    with open(EDGE_NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_memorization() -> dict[str, bool]:
    if os.path.exists(MEMORIZATION_FILE):
        try:
            with open(MEMORIZATION_FILE, encoding="utf-8") as f:
                raw = json.load(f)
            out: dict[str, bool] = {}
            for k, v in raw.items():
                if isinstance(v, bool):
                    out[str(k)] = v
                elif v in (1, "1", "true", "True", "memorized"):
                    out[str(k)] = True
                elif v in (0, "0", "false", "False", "not"):
                    out[str(k)] = False
            return out
        except Exception:
            pass
    return {}


def save_memorization_file(data: dict[str, bool]) -> None:
    with open(MEMORIZATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_daily_brain_snapshot() -> None:
    """Overwrite today's JSON snapshot whenever the graph is saved (per-calendar-day brain)."""
    d = date.today().isoformat()
    try:
        os.makedirs(DAILY_BRAIN_DIR, exist_ok=True)
        path = os.path.join(DAILY_BRAIN_DIR, f"brain_{d}.json")
        payload = {
            "date": d,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "nodes": st.session_state.nodes,
            "edges": st.session_state.edges,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass


_RE_GRAPH_ARCHIVE = re.compile(r"^graph_(\d{4}-\d{2}-\d{2})\.json$")
_RE_BRAIN_DAY = re.compile(r"^brain_(\d{4}-\d{2}-\d{2})\.json$")


def iter_saved_graph_dates() -> list[str]:
    """All ISO dates that have a graph snapshot in archive and/or brain_by_day."""
    found: set[str] = set()
    for d in (GRAPH_ARCHIVE_DIR, DAILY_BRAIN_DIR):
        try:
            os.makedirs(d, exist_ok=True)
            for name in os.listdir(d):
                m = _RE_GRAPH_ARCHIVE.match(name) if d == GRAPH_ARCHIVE_DIR else _RE_BRAIN_DAY.match(name)
                if m:
                    found.add(m.group(1))
        except OSError:
            pass
    return sorted(found, reverse=True)


def load_graph_payload_for_date(iso_date: str) -> dict[str, list] | None:
    """Return {'nodes','edges'} from graph_archive first, else brain_by_day."""
    arc = os.path.join(GRAPH_ARCHIVE_DIR, f"graph_{iso_date}.json")
    if os.path.isfile(arc):
        try:
            with open(arc, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d.get("nodes"), list) and isinstance(d.get("edges"), list):
                return {"nodes": d["nodes"], "edges": d["edges"]}
        except Exception:
            pass
    brain = os.path.join(DAILY_BRAIN_DIR, f"brain_{iso_date}.json")
    if os.path.isfile(brain):
        try:
            with open(brain, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d.get("nodes"), list) and isinstance(d.get("edges"), list):
                return {"nodes": d["nodes"], "edges": d["edges"]}
        except Exception:
            pass
    return None


def write_graph_calendar_snapshot(iso_date: str, nodes: list, edges: list) -> None:
    """Write the same graph to graph_archive (plain) and brain_by_day (with metadata)."""
    os.makedirs(GRAPH_ARCHIVE_DIR, exist_ok=True)
    os.makedirs(DAILY_BRAIN_DIR, exist_ok=True)
    arc = os.path.join(GRAPH_ARCHIVE_DIR, f"graph_{iso_date}.json")
    with open(arc, "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": edges}, f, indent=2)
    brain = os.path.join(DAILY_BRAIN_DIR, f"brain_{iso_date}.json")
    payload = {
        "date": iso_date,
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "nodes": nodes,
        "edges": edges,
    }
    with open(brain, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def parse_uploaded_graph_json(raw: dict) -> tuple[list, list] | None:
    """Accept connections-style or brain snapshot JSON."""
    n, e = raw.get("nodes"), raw.get("edges")
    if isinstance(n, list) and isinstance(e, list):
        return n, e
    return None


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
def init_state():
    conn = load_connections()
    defaults = {
        "nodes": conn["nodes"],
        "edges": conn["edges"],
        "active_verse": None,       # e.g. "John 3:16"
        "book": "John",
        "chapter": 3,
        "chapter_verses": [],       # list of {verse, text}
        "selected_verse_num": None,
        "search_ref": "",
        "search_result": None,      # {reference, text}
        "graph_selected": None,     # node id clicked in graph
        "status_msg": "",
        "status_type": "info",
        "auto_link_to_active": True,
        "view_mode": "Split",  # Split | Reader | Brain
        "split_right_panel": _split_right_panel_from_meta(),  # restored after full-page verse HTML tap (?reader_inspector=)
        "_reader_loc": None,  # (book, chapter) — detect changes to clear cached verses
        "verse_memorization": load_memorization(),  # clean_ref -> True memorized / False not
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


maybe_daily_graph_rollover()
init_state()


@st.cache_resource
def _bible_http_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "Accept": "application/json",
            "User-Agent": "Christology-BibleReader/1.0",
            "Accept-Encoding": "gzip, deflate",
        }
    )
    return s


def consume_graph_nav_from_query() -> None:
    """Open reader + text inspector after tap on embedded graph (URL ?graph_nav=...)."""
    q = st.query_params
    if "graph_nav" not in q:
        return
    raw = q["graph_nav"]
    if isinstance(raw, (list, tuple)):
        raw = raw[0] if raw else ""
    ref = re.sub(r"\s+", " ", unquote(str(raw)).strip())
    m = re.match(r"^(.+?)\s+(\d+):(\d+)$", ref)
    if m:
        # Inspector data updates; right column tab stays whatever you chose (Graph vs Text inspector).
        st.session_state._graph_node_panel_ref = ref
        apply_ref_to_reader(ref)
        sync_graph_inspector_pick_from_ref(ref)
    try:
        del st.query_params["graph_nav"]
    except Exception:
        try:
            st.query_params.pop("graph_nav", None)
        except Exception:
            pass


def consume_reader_inspector_from_query() -> None:
    """Split view: hover/click on verse text sets ?reader_inspector= — sync focus ref (keeps Graph vs inspector toggle)."""
    q = st.query_params
    if "reader_inspector" not in q:
        return
    raw = q["reader_inspector"]
    if isinstance(raw, (list, tuple)):
        raw = raw[0] if raw else ""
    ref = re.sub(r"\s+", " ", unquote(str(raw)).strip())
    m = re.match(r"^(.+?)\s+(\d+):(\d+)$", ref)
    if m:
        prev = st.session_state.get("_graph_node_panel_ref")
        st.session_state._graph_node_panel_ref = ref
        sync_graph_inspector_pick_from_ref(ref)
        if ref != prev:
            vs = int(m.group(3))
            st.session_state.active_verse = ref
            st.session_state.selected_verse_num = vs
    try:
        del st.query_params["reader_inspector"]
    except Exception:
        try:
            st.query_params.pop("reader_inspector", None)
        except Exception:
            pass


def apply_pending_schedule_jump() -> None:
    """Apply schedule 'open chapter' queued by on_click (runs before widgets; fixes left-column-already-ran bug)."""
    j = st.session_state.pop("_pending_schedule_jump", None)
    if not j:
        return
    b = j.get("book")
    ch = int(j.get("chapter", 1))
    if not b or b not in ALL_BOOKS:
        return
    max_c = CHAPTERS_PER_BOOK.get(b, 1)
    ch = max(1, min(ch, max_c))
    st.session_state.book = b
    st.session_state.chapter = ch
    st.session_state.chapter_verses = []
    st.session_state.selected_verse_num = 1
    st.session_state._reader_loc = (b, ch)
    # Show reader beside graph (was invisible in Brain-only view)
    st.session_state.view_mode = "Split"


def _on_schedule_reading_click(reading_label: str) -> None:
    """Button callback — runs before script body so reader widgets see the new book/chapter."""
    book_name, ch_num = parse_schedule_ref(reading_label)
    if not book_name or not ch_num or book_name not in ALL_BOOKS:
        st.session_state.status_msg = f"Could not open: {reading_label!r}"
        st.session_state.status_type = "warning"
        return
    max_c = CHAPTERS_PER_BOOK.get(book_name, 1)
    ch_num = max(1, min(int(ch_num), max_c))
    st.session_state._pending_schedule_jump = {"book": book_name, "chapter": ch_num}


@st.cache_data(show_spinner=False)
def load_tsk_edges() -> list[dict]:
    """Load local TSK-style cross-reference edges if available."""
    for path in TSK_EDGES_FILE_CANDIDATES:
        if os.path.exists(path):
            rows = []
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        src = (r.get("source") or "").strip()
                        tgt = (r.get("target") or "").strip()
                        w = r.get("weight", 1)
                        if src and tgt:
                            try:
                                wt = int(float(w))
                            except Exception:
                                wt = 1
                            rows.append({"source": src, "target": tgt, "weight": wt})
                return rows
            except Exception:
                return []
    return []


def _tsk_csv_mtime() -> float:
    for path in TSK_EDGES_FILE_CANDIDATES:
        if os.path.exists(path):
            return _json_file_mtime(path)
    return 0.0


@st.cache_data(show_spinner=False)
def _tsk_neighbors_by_id(_csv_mtime: float) -> dict[str, tuple[tuple[str, int], ...]]:
    """TSK id → neighbors (tsk_id, weight) sorted by weight desc; built once per CSV revision."""
    edges = load_tsk_edges()
    if not edges:
        return {}
    merged: dict[str, dict[str, int]] = {}
    for e in edges:
        s, t = e["source"], e["target"]
        wt = int(e["weight"])
        merged.setdefault(s, {})
        merged.setdefault(t, {})
        merged[s][t] = max(merged[s].get(t, 0), wt)
        merged[t][s] = max(merged[t].get(s, 0), wt)
    out: dict[str, tuple[tuple[str, int], ...]] = {}
    for k, d in merged.items():
        out[k] = tuple(sorted(d.items(), key=lambda x: (-x[1], x[0])))
    return out


_REF_BOOK_CH_VERSE_RANGE = re.compile(r"^(.+?)\s+(\d+):(\d+)(?:\s*-\s*(\d+))?\s*$")


def _kjv_local_mtime() -> float:
    try:
        if os.path.isfile(KJV_LOCAL_FILE) and os.path.getsize(KJV_LOCAL_FILE) > 64:
            return os.path.getmtime(KJV_LOCAL_FILE)
    except OSError:
        pass
    return 0.0


@st.cache_data(show_spinner=False)
def _kjv_local_document(_mtime: float) -> dict | None:
    if _mtime <= 0:
        return None
    try:
        with open(KJV_LOCAL_FILE, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def _kjv_chapter_rows_from_doc(doc: dict, book: str, chapter: int) -> list[dict]:
    ch_map = doc.get(book)
    if not isinstance(ch_map, dict):
        return []
    raw_rows = ch_map.get(str(chapter))
    if raw_rows is None:
        raw_rows = ch_map.get(chapter)
    if not isinstance(raw_rows, list):
        return []
    out: list[dict] = []
    for row in raw_rows:
        if not isinstance(row, dict):
            continue
        try:
            vn = int(row["verse"])
            tx = str(row.get("text", "")).strip()
        except (KeyError, TypeError, ValueError):
            continue
        if tx:
            out.append({"verse": vn, "text": tx})
    return sorted(out, key=lambda x: int(x["verse"]))


def _kjv_passage_dict_from_doc(doc: dict, ref: str) -> dict | None:
    m = _REF_BOOK_CH_VERSE_RANGE.match(ref)
    if not m:
        return None
    book, ch, v_lo, v_hi = m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4)
    v_hi = int(v_hi) if v_hi else v_lo
    if v_hi < v_lo:
        v_lo, v_hi = v_hi, v_lo
    if book not in ALL_BOOKS:
        return None
    max_c = CHAPTERS_PER_BOOK.get(book, 1)
    ch = max(1, min(ch, max_c))
    rows = _kjv_chapter_rows_from_doc(doc, book, ch)
    if not rows:
        return None
    by_v: dict[int, str] = {}
    for row in rows:
        try:
            by_v[int(row["verse"])] = row["text"].strip()
        except (TypeError, ValueError, KeyError):
            pass
    parts: list[str] = []
    for vn in range(v_lo, v_hi + 1):
        t = by_v.get(vn)
        if t:
            parts.append(t)
    if not parts:
        return None
    label = f"{book} {ch}:{v_lo}" + (f"-{v_hi}" if v_hi != v_lo else "")
    return {"reference": label, "text": " ".join(parts)}


def download_kjv_to_local_file() -> tuple[bool, str]:
    """Fetch public-domain KJV JSON, normalize to kjv_by_chapter.json (one-time; ~1–2 MB)."""
    try:
        r = _bible_http_session().get(KJV_SOURCE_JSON_URL, timeout=180)
        if r.status_code != 200:
            return False, f"Download failed: HTTP {r.status_code}"
        arr = r.json()
        if not isinstance(arr, list):
            return False, "Unexpected JSON (expected a list of books)."
    except Exception as e:
        return False, str(e)
    out: dict[str, dict] = {}
    for book in arr:
        if not isinstance(book, dict):
            continue
        name = book.get("name")
        chapters = book.get("chapters")
        if not name or not isinstance(chapters, list):
            continue
        if name not in ALL_BOOKS:
            continue
        out[name] = {}
        for ci, verse_list in enumerate(chapters, start=1):
            if not isinstance(verse_list, list):
                continue
            rows: list[dict] = []
            for vi, text in enumerate(verse_list, start=1):
                t = str(text).strip() if text is not None else ""
                if t:
                    rows.append({"verse": vi, "text": t})
            if rows:
                out[name][str(ci)] = rows
    try:
        with open(KJV_LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    except OSError as e:
        return False, str(e)
    for _fn in (_kjv_local_document, fetch_chapter, fetch_verse):
        try:
            _fn.clear()
        except Exception:
            pass
    return True, f"Saved **{len(out)}** books to `{os.path.basename(KJV_LOCAL_FILE)}` — reloads use disk (fast)."


# ─────────────────────────────────────────────────────────────
# BIBLE API
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=7200, show_spinner=False)
def fetch_chapter(book: str, chapter: int, *, _api_bust: int = 6) -> list[dict]:
    """Local KJV file first; else bible-api.com KJV then WEB."""
    lm = _kjv_local_mtime()
    if lm > 0:
        doc = _kjv_local_document(lm)
        if doc:
            rows = _kjv_chapter_rows_from_doc(doc, book, int(chapter))
            if rows:
                return rows
    ref = f"{book}+{chapter}"
    for attempt in range(3):
        for tr in ("kjv", "web"):
            try:
                r = _bible_http_session().get(
                    f"{API_BASE}/{ref}?translation={tr}", timeout=22
                )
                if r.status_code == 429:
                    time.sleep(2.2 * (attempt + 1))
                    continue
                if r.status_code != 200:
                    continue
                data = r.json()
                verses = data.get("verses", [])
                if not verses:
                    continue
                return [{"verse": v["verse"], "text": v["text"].strip()} for v in verses]
            except Exception:
                time.sleep(0.35 * (attempt + 1))
                continue
        if attempt < 2:
            time.sleep(0.5 * (attempt + 1))
    return []


def _normalize_scripture_ref_string(ref: str) -> str:
    s = re.sub(r"\s+", " ", (ref or "").strip())
    for dash in ("\u2013", "\u2014", "\u2212", "–", "—"):
        s = s.replace(dash, "-")
    return s


def _canonicalize_book_in_ref(ref: str) -> str:
    """Align common labels with ALL_BOOKS / bible-api.com (graph + TSK quirks)."""
    s = re.sub(r"\s+", " ", (ref or "").strip())
    for pat, repl in (
        (re.compile(r"^III\s+", re.I), "3 "),
        (re.compile(r"^II\s+", re.I), "2 "),
        (re.compile(r"^I\s+", re.I), "1 "),
    ):
        if pat.match(s):
            s = pat.sub(repl, s)
            break
    fixes = (
        ("Psalm ", "Psalms "),
        ("Psalms.", "Psalms "),
        ("Proverb ", "Proverbs "),
        ("Proverbs.", "Proverbs "),
        ("Song of Songs ", "Song of Solomon "),
    )
    for wrong, right in fixes:
        if s.startswith(wrong):
            s = right + s[len(wrong) :]
            break
    return s


def _fetch_verse_via_chapter_cache(ref: str) -> dict | None:
    """If the single-ref API fails, build text from fetch_chapter (same cache as reader)."""
    m = _REF_BOOK_CH_VERSE_RANGE.match(ref)
    if not m:
        return None
    book, ch, v_lo, v_hi = m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4)
    v_hi = int(v_hi) if v_hi else v_lo
    if v_hi < v_lo:
        v_lo, v_hi = v_hi, v_lo
    if book not in ALL_BOOKS:
        return None
    max_c = CHAPTERS_PER_BOOK.get(book, 1)
    ch = max(1, min(ch, max_c))
    rows = fetch_chapter(book, ch)
    if not rows:
        return None
    by_v: dict[int, str] = {}
    for r in rows:
        try:
            by_v[int(r["verse"])] = r["text"].strip()
        except (TypeError, ValueError, KeyError):
            pass
    parts: list[str] = []
    for vn in range(v_lo, v_hi + 1):
        t = by_v.get(vn)
        if t:
            parts.append(t)
    if not parts:
        return None
    label = f"{book} {ch}:{v_lo}" + (f"-{v_hi}" if v_hi != v_lo else "")
    return {"reference": label, "text": " ".join(parts)}


@st.cache_data(ttl=7200, show_spinner=False)
def fetch_verse(reference: str, *, _cache_bust: int = 12) -> dict | None:
    """Local KJV file first; else bible-api KJV/WEB; then chapter cache."""
    ref = _canonicalize_book_in_ref(_normalize_scripture_ref_string(reference))
    if not ref:
        return None

    lm = _kjv_local_mtime()
    if lm > 0:
        doc = _kjv_local_document(lm)
        if doc:
            local_passage = _kjv_passage_dict_from_doc(doc, ref)
            if local_passage:
                return local_passage

    encodings = (
        ref.replace(" ", "+").replace(":", "%3A"),
        quote(ref, safe=""),
    )
    seen_pairs: set[str] = set()
    for tr in ("kjv", "web"):
        for ref_encoded in encodings:
            pair_key = f"{tr}\x1e{ref_encoded}"
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)
            try:
                r = _bible_http_session().get(
                    f"{API_BASE}/{ref_encoded}?translation={tr}", timeout=22
                )
                if r.status_code != 200:
                    continue
                data = r.json()
                verses = data.get("verses", [])
                if not verses:
                    continue

                def _vk(v):
                    try:
                        return int(v.get("verse", 0))
                    except (TypeError, ValueError):
                        return 0

                ordered = sorted(verses, key=_vk)
                full_text = " ".join(v["text"].strip() for v in ordered)
                return {"reference": data.get("reference", ref), "text": full_text}
            except Exception:
                continue

    return _fetch_verse_via_chapter_cache(ref)


@st.cache_data(ttl=7200, show_spinner=False)
def xref_preview_tooltip(display_ref: str) -> str:
    """Short KJV snippet for cross-ref hover (Streamlit widget help text)."""
    r = (display_ref or "").strip()
    if not r:
        return ""
    data = fetch_verse(r)
    if not data:
        return f"{r} — Bible text not available (offline or unknown ref)."
    t = re.sub(r"\s+", " ", data["text"]).strip()
    snippet = t[:400] + ("…" if len(t) > 400 else "")
    return f"{data['reference']}: {snippet}"


def clean_ref(ref: str) -> str:
    """Normalize a reference string to a node ID: 'John 3:16' → 'john_3_16'."""
    return re.sub(r"[:\s]+", "_", ref.strip().lower())


def sync_graph_inspector_pick_from_ref(ref: str) -> None:
    """Align the Show group selectbox with a verse ref (canonical node data['ref'])."""
    key = "graph_inspector_manual_pick"
    r = re.sub(r"\s+", " ", (ref or "").strip())
    if not r:
        return
    want = clean_ref(r)
    for n in st.session_state.get("nodes", []):
        nr = (n.get("data") or {}).get("ref")
        if nr and clean_ref(nr) == want:
            st.session_state[key] = nr
            return


def sync_split_inspector_content_from_reader_ref(ref: str) -> None:
    """In Split view, keep the text inspector focus ref in sync with the reader (does not change Graph vs inspector)."""
    if st.session_state.get("view_mode") != "Split":
        return
    r = re.sub(r"\s+", " ", (ref or "").strip())
    if not r:
        return
    st.session_state._graph_node_panel_ref = r
    sync_graph_inspector_pick_from_ref(r)


def ref_is_nt(ref: str) -> bool:
    r = ref.lower()
    return any(b.lower() in r for b in BOOKS_NT)


def node_fill_for_mem(ref: str, memorized: bool | None) -> str:
    """Graph node fill: green = memorized, slate = explicitly not, cyan/amber = unset by testament."""
    if memorized is True:
        return "#10b981"
    if memorized is False:
        return "#64748b"
    return "#38bdf8" if ref_is_nt(ref) else "#f59e0b"


def sync_node_colors_in_session() -> None:
    """Apply verse_memorization + testament defaults to every node’s data.color."""
    vm = st.session_state.get("verse_memorization") or {}
    for n in st.session_state.nodes:
        ref = n.get("data", {}).get("ref") or ""
        nid = n.get("data", {}).get("id") or clean_ref(ref)
        m = vm.get(nid)
        n["data"]["color"] = node_fill_for_mem(ref, m)


# ─────────────────────────────────────────────────────────────
# GRAPH HELPERS
# ─────────────────────────────────────────────────────────────
def node_exists(ref: str) -> bool:
    nid = clean_ref(ref)
    return any(n["data"]["id"] == nid for n in st.session_state.nodes)


def node_ref_by_id(nid: str) -> str | None:
    for n in st.session_state.nodes:
        if n["data"]["id"] == nid:
            return n["data"].get("ref")
    return None


def canonical_edge_key(ref_a: str, ref_b: str) -> str:
    x, y = sorted([clean_ref(ref_a), clean_ref(ref_b)])
    return f"{x}___{y}"


def neighbor_refs_for(ref: str) -> list[str]:
    """Display refs of nodes connected to `ref` in the current graph."""
    nid = clean_ref(ref)
    out: list[str] = []
    seen: set[str] = set()
    for e in st.session_state.edges:
        s, t = e["data"]["source"], e["data"]["target"]
        other = None
        if s == nid:
            other = t
        elif t == nid:
            other = s
        if other:
            r = node_ref_by_id(other)
            if r and r not in seen:
                seen.add(r)
                out.append(r)
    return out


def one_hop_group_refs(center_ref: str) -> list[str]:
    """Tapped verse first, then every 1-hop neighbor (unique by clean_ref)."""
    r = re.sub(r"\s+", " ", (center_ref or "").strip())
    if not r:
        return []
    out: list[str] = [r]
    seen: set[str] = {clean_ref(r)}
    for nref in neighbor_refs_for(r):
        k = clean_ref(nref)
        if k not in seen:
            seen.add(k)
            out.append(nref)
    return out


def apply_ref_to_reader(ref: str) -> bool:
    """Jump reader to ref if it parses as Book C:V in ALL_BOOKS."""
    ref = re.sub(r"\s+", " ", (ref or "").strip())
    m = re.match(r"^(.+?)\s+(\d+):(\d+)$", ref)
    if not m:
        return False
    b, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
    if b not in ALL_BOOKS:
        return False
    st.session_state.book = b
    st.session_state.chapter = ch
    st.session_state.selected_verse_num = vs
    st.session_state.chapter_verses = []
    st.session_state.active_verse = ref
    st.session_state._reader_loc = (b, ch)
    st.session_state.view_mode = "Split"
    st.session_state._scroll_verse_num = vs
    sync_split_inspector_content_from_reader_ref(ref)
    return True


def apply_pending_graph_group_open() -> None:
    """After Show group + rerun: set inspector ref + reader jump (runs before header widgets)."""
    ref = st.session_state.pop("_pending_open_graph_group", None)
    if not ref or ref == GRAPH_INSPECTOR_PICK_PLACEHOLDER:
        return
    ref = re.sub(r"\s+", " ", str(ref).strip())
    if not ref:
        return
    st.session_state._graph_node_panel_ref = ref
    apply_ref_to_reader(ref)
    sync_graph_inspector_pick_from_ref(ref)


# URL graph tap + queued Show group need apply_ref_to_reader — run these only after it is defined.
consume_graph_nav_from_query()
consume_reader_inspector_from_query()
apply_pending_graph_group_open()
apply_pending_schedule_jump()


def add_node(ref: str, label: str | None = None):
    if node_exists(ref):
        return
    nid = clean_ref(ref)
    vm = st.session_state.get("verse_memorization") or {}
    color = node_fill_for_mem(ref, vm.get(nid))
    st.session_state.nodes.append({
        "data": {"id": nid, "label": label or ref, "ref": ref, "color": color}
    })
    _persist()


def add_edge(ref1: str, ref2: str):
    id1, id2 = clean_ref(ref1), clean_ref(ref2)
    eid = f"{id1}___{id2}"
    rev = f"{id2}___{id1}"
    exists = any(e["data"]["id"] in {eid, rev} for e in st.session_state.edges)
    if not exists and id1 != id2:
        st.session_state.edges.append({
            "data": {"id": eid, "source": id1, "target": id2}
        })
        _persist()


def build_linear_chapter_chain(book: str, chapter: int, verses: list) -> tuple[int, int, int]:
    """
    One node per verse, directed edges verse N → verse N+1 through the chapter (linear / snake chain).
    Returns (verse_count, nodes_added, edges_added).
    """
    if not verses:
        return 0, 0, 0
    ordered = sorted(verses, key=lambda x: int(x["verse"]))
    vm = st.session_state.get("verse_memorization") or {}
    existing_ids = {n["data"]["id"] for n in st.session_state.nodes}
    edge_ids = {e["data"]["id"] for e in st.session_state.edges}
    nodes_added = 0
    edges_added = 0

    refs = [f"{book} {chapter}:{int(v['verse'])}" for v in ordered]

    for ref in refs:
        nid = clean_ref(ref)
        if nid not in existing_ids:
            color = node_fill_for_mem(ref, vm.get(nid))
            st.session_state.nodes.append({
                "data": {"id": nid, "label": ref, "ref": ref, "color": color}
            })
            existing_ids.add(nid)
            nodes_added += 1

    for i in range(len(refs) - 1):
        id1, id2 = clean_ref(refs[i]), clean_ref(refs[i + 1])
        eid = f"{id1}___{id2}"
        if eid not in edge_ids and id1 != id2:
            st.session_state.edges.append({
                "data": {"id": eid, "source": id1, "target": id2}
            })
            edge_ids.add(eid)
            edges_added += 1

    sync_node_colors_in_session()
    save_connections({"nodes": st.session_state.nodes, "edges": st.session_state.edges})
    save_daily_brain_snapshot()
    return len(refs), nodes_added, edges_added


def add_node_and_maybe_link(ref: str, label: str | None = None):
    """Add node and auto-link to active verse when enabled."""
    was_new = not node_exists(ref)
    add_node(ref, label=label)
    av = st.session_state.active_verse
    if (
        was_new
        and st.session_state.auto_link_to_active
        and av
        and clean_ref(av) != clean_ref(ref)
    ):
        add_edge(av, ref)


def link_crossref_to_active(av: str, target_ref: str, note: str = "") -> None:
    """Fetch target if possible, add nodes, edge active↔target, rerun."""
    result = fetch_verse(target_ref.strip())
    add_node(av)
    if result:
        add_node_and_maybe_link(result["reference"])
        add_edge(av, result["reference"])
        msg = f"Linked {av} ↔ {result['reference']}"
    else:
        add_node_and_maybe_link(target_ref.strip())
        add_edge(av, target_ref.strip())
        msg = f"Linked {av} ↔ {target_ref.strip()} (text unresolved)"
    if note:
        msg = f"{msg} ({note})"
    st.session_state.status_msg = msg
    st.session_state.status_type = "success"
    st.rerun()


def top_tsk_related(reference: str, limit: int = 12) -> list[tuple[str, int]]:
    """Return top related verses as display refs ('Genesis 1:1') + weight from TSK CSV."""
    if not reference:
        return []
    tsk_self = display_ref_to_tsk_id(reference.strip())
    if not tsk_self:
        return []
    ranked = _tsk_neighbors_by_id(_tsk_csv_mtime()).get(tsk_self)
    if not ranked:
        return []
    ref_strip = reference.strip()
    out: list[tuple[str, int]] = []
    seen: set[str] = set()
    for tsk_id, wt in ranked:
        if len(out) >= limit:
            break
        disp = tsk_id_to_display_ref(tsk_id)
        if not disp or disp == ref_strip:
            continue
        key = clean_ref(disp)
        if key in seen:
            continue
        seen.add(key)
        out.append((disp, wt))
    return out


_REF_BOOK_CH_VERSE = re.compile(r"^(.+?)\s+(\d+):(\d+)$")


def _schedule_chapter_key_for_node_ref(ref: str) -> str | None:
    """Return 'Book|chapter' if ref parses as a single verse, else None."""
    r = re.sub(r"\s+", " ", (ref or "").strip())
    m = _REF_BOOK_CH_VERSE.match(r)
    if not m:
        return None
    book, ch = m.group(1).strip(), int(m.group(2))
    if book not in ALL_BOOKS:
        return None
    return f"{book}|{ch}"


def link_top_tsk_for_today_schedule_nodes(limit: int = 10) -> tuple[int, int, int]:
    """
    For each graph node whose verse lies in today's reading chapters (snake / line layout set),
    add up to `limit` TSK cross-reference targets as nodes and undirected edges.

    Returns (sources_matched, nodes_added, edges_added). If TSK CSV is missing, returns (-1, 0, 0).
    """
    chapter_keys = set(today_schedule_chapter_keys())
    if not chapter_keys:
        return 0, 0, 0
    if not load_tsk_edges():
        return -1, 0, 0

    vm = st.session_state.get("verse_memorization") or {}
    existing_ids = {n["data"]["id"] for n in st.session_state.nodes}
    pair_seen = {
        tuple(sorted((e["data"]["source"], e["data"]["target"])))
        for e in st.session_state.edges
    }

    nodes_added = 0
    edges_added = 0
    sources_matched = 0

    for n in st.session_state.nodes:
        ref = (n.get("data") or {}).get("ref") or ""
        ref = re.sub(r"\s+", " ", ref.strip())
        ck = _schedule_chapter_key_for_node_ref(ref)
        if not ck or ck not in chapter_keys:
            continue
        sources_matched += 1
        src_id = clean_ref(ref)
        for target_ref, _wt in top_tsk_related(ref, limit=limit):
            tid = clean_ref(target_ref)
            if tid not in existing_ids:
                color = node_fill_for_mem(target_ref, vm.get(tid))
                st.session_state.nodes.append({
                    "data": {"id": tid, "label": target_ref, "ref": target_ref, "color": color}
                })
                existing_ids.add(tid)
                nodes_added += 1
            pk = tuple(sorted((src_id, tid)))
            if src_id == tid or pk in pair_seen:
                continue
            pair_seen.add(pk)
            eid = f"{src_id}___{tid}"
            st.session_state.edges.append({
                "data": {"id": eid, "source": src_id, "target": tid}
            })
            edges_added += 1

    if nodes_added or edges_added:
        sync_node_colors_in_session()
        save_connections({"nodes": st.session_state.nodes, "edges": st.session_state.edges})
        save_daily_brain_snapshot()

    return sources_matched, nodes_added, edges_added


def remove_node(ref: str):
    nid = clean_ref(ref)
    st.session_state.nodes = [n for n in st.session_state.nodes if n["data"]["id"] != nid]
    st.session_state.edges = [
        e for e in st.session_state.edges
        if e["data"]["source"] != nid and e["data"]["target"] != nid
    ]
    if st.session_state.active_verse and clean_ref(st.session_state.active_verse) == nid:
        st.session_state.active_verse = None
    _persist()


def _persist():
    sync_node_colors_in_session()
    save_connections({"nodes": st.session_state.nodes, "edges": st.session_state.edges})
    save_daily_brain_snapshot()


def render_graph_calendar_sidebar() -> None:
    """List saved daily graphs, load/download, snapshot to a date, import JSON into a date."""
    st.caption(
        "End-of-day rollovers go to `graph_archive/graph_YYYY-MM-DD.json`. "
        "Each save also updates `brain_by_day/brain_YYYY-MM-DD.json`. "
        "Use this panel to open any day, download it, or file uploads into a date."
    )
    dates = iter_saved_graph_dates()
    ph = "— pick a saved date —"
    labels = [ph] + dates if dates else [ph]
    pick = st.selectbox("Saved calendar dates", labels, key="gcal_pick_date", disabled=not dates)
    payload = load_graph_payload_for_date(pick) if pick != ph else None
    if pick != ph and payload is not None:
        st.caption(f"**{pick}** — {len(payload['nodes'])} nodes · {len(payload['edges'])} edges")
        dl = json.dumps({"nodes": payload["nodes"], "edges": payload["edges"]}, indent=2)
        st.download_button(
            "⬇ Download this day (JSON)",
            data=dl,
            file_name=f"nexus_graph_{pick}.json",
            mime="application/json",
            key="gcal_dl_day",
        )
        if st.button("Load this day into the graph", key="gcal_load_day"):
            st.session_state.nodes = payload["nodes"]
            st.session_state.edges = payload["edges"]
            sync_node_colors_in_session()
            _persist()
            st.session_state.status_msg = f"Loaded graph from **{pick}** (saved to connections.json)."
            st.session_state.status_type = "success"
            st.rerun()
    elif pick != ph:
        st.warning("Could not read that snapshot file.")

    st.markdown("**Save current graph** under a date (archive + brain folder).")
    save_d = st.date_input("Date for snapshot", value=date.today(), key="gcal_save_date")
    if st.button("Write snapshot for this date", key="gcal_write_snap"):
        write_graph_calendar_snapshot(
            save_d.isoformat(),
            list(st.session_state.nodes),
            list(st.session_state.edges),
        )
        st.session_state.status_msg = f"Saved graph snapshot for **{save_d.isoformat()}**."
        st.session_state.status_type = "success"
        st.rerun()

    st.markdown("**Upload** a saved JSON into the calendar")
    up = st.file_uploader(
        "Graph JSON (nodes + edges)",
        type="json",
        key="gcal_upload_file",
        help="Same shape as connections.json or a brain_*.json export.",
    )
    up_d = st.date_input("Store under this date", value=date.today(), key="gcal_upload_date")
    also_load = st.checkbox("Also replace the live graph", value=False, key="gcal_upload_replace")
    if st.button("Import file into calendar", key="gcal_import_btn"):
        if not up:
            st.session_state.status_msg = "Choose a JSON file first."
            st.session_state.status_type = "warning"
            st.rerun()
        try:
            raw = json.load(up)
            parsed = parse_uploaded_graph_json(raw)
            if not parsed:
                st.session_state.status_msg = "JSON must contain nodes and edges arrays."
                st.session_state.status_type = "warning"
                st.rerun()
            nodes, edges = parsed
            iso = up_d.isoformat()
            write_graph_calendar_snapshot(iso, nodes, edges)
            if also_load:
                st.session_state.nodes = nodes
                st.session_state.edges = edges
                sync_node_colors_in_session()
                _persist()
                st.session_state.status_msg = (
                    f"Imported graph into **{iso}** and loaded it as the live graph."
                )
            else:
                st.session_state.status_msg = f"Imported graph into calendar date **{iso}** (live graph unchanged)."
            st.session_state.status_type = "success"
            st.rerun()
        except Exception as e:
            st.session_state.status_msg = f"Import failed: {e}"
            st.session_state.status_type = "warning"
            st.rerun()


def cytoscape_elements():
    sync_node_colors_in_session()
    return st.session_state.nodes + st.session_state.edges


def cytoscape_elements_with_hover_text() -> list:
    """Graph payload with data.verse_text for node hover tooltips (session graph unchanged)."""
    sync_node_colors_in_session()
    out: list = []
    for n in st.session_state.nodes:
        data = dict(n.get("data") or {})
        ref = data.get("ref")
        if ref:
            fv = fetch_verse(str(ref).strip())
            raw = (fv or {}).get("text") or ""
            raw = re.sub(r"\s+", " ", raw).strip()
            if len(raw) > 1200:
                raw = raw[:1197] + "…"
            data["verse_text"] = raw
        else:
            data["verse_text"] = ""
        out.append({"data": data})
    out.extend(st.session_state.edges)
    return out


CYTOSCAPE_STYLESHEET: list[dict] = [
    {
        "selector": "node",
        "style": {
            "background-color": "data(color)",
            "label": "data(label)",
            "color": "#c8d4e4",
            "font-size": "10px",
            "font-family": "JetBrains Mono, monospace",
            "text-valign": "bottom",
            "text-margin-y": "4px",
            "width": "32px",
            "height": "32px",
            "border-width": "1.5px",
            "border-color": "rgba(34, 211, 238, 0.35)",
            "text-wrap": "wrap",
            "text-max-width": "90px",
        },
    },
    {
        "selector": "node:selected",
        "style": {
            "border-color": "#a78bfa",
            "border-width": "3px",
            "background-color": "#a78bfa",
            "width": "38px",
            "height": "38px",
        },
    },
    {
        "selector": "edge",
        "style": {
            "line-color": "rgba(56, 189, 248, 0.35)",
            "width": 1.15,
            "opacity": 0.78,
            "curve-style": "unbundled-bezier",
            "target-arrow-color": "rgba(167, 139, 250, 0.55)",
            "target-arrow-shape": "triangle",
            "arrow-scale": 0.45,
        },
    },
    {
        "selector": "edge:selected",
        "style": {"line-color": "#22d3ee", "width": 2, "opacity": 1},
    },
]


def render_brain_graph_interactive(elements: list, stylesheet: list, height: int) -> None:
    """Full Cytoscape.js in an iframe: wheel zoom, pan, toolbar; tap node → ?graph_nav=… reload."""
    _jsep = (",", ":")
    el_json = json.dumps(elements, ensure_ascii=False, separators=_jsep)
    sty_json = json.dumps(stylesheet, ensure_ascii=False, separators=_jsep)
    sk_json = json.dumps(today_schedule_chapter_keys(), ensure_ascii=False, separators=_jsep)
    h = max(300, int(height))
    script = (
        "var nexusScheduleChapterKeys = new Set("
        + sk_json
        + ");\nvar elements = "
        + el_json
        + ";\nvar stylesheet = "
        + sty_json
        + ";\n"
        + """
function nexusChapterLineLayout(elements) {
  var scheduleSet = nexusScheduleChapterKeys;
  var useScheduleOnly = scheduleSet && scheduleSet.size > 0;
  var nodes = [];
  var edges = [];
  elements.forEach(function (el) {
    if (el.data && el.data.source != null && el.data.target != null) edges.push(el);
    else nodes.push(el);
  });
  var adj = {};
  edges.forEach(function (e) {
    var s = e.data.source, t = e.data.target;
    if (!adj[s]) adj[s] = [];
    if (!adj[t]) adj[t] = [];
    adj[s].push(t);
    adj[t].push(s);
  });
  var lineGroups = {};
  nodes.forEach(function (el) {
    var ref = (el.data && el.data.ref) || '';
    var m = ref.match(/^(.+?)\\s+(\\d+):(\\d+)$/);
    if (!m) return;
    var key = m[1].trim() + '|' + m[2];
    if (useScheduleOnly && !scheduleSet.has(key)) return;
    var vs = parseInt(m[3], 10);
    if (!lineGroups[key]) lineGroups[key] = [];
    lineGroups[key].push({ el: el, vs: vs });
  });
  var row = 0;
  var maxX = 0;
  var dx = 520;
  var dy = 720;
  Object.keys(lineGroups).sort().forEach(function (k) {
    var arr = lineGroups[k].sort(function (a, b) { return a.vs - b.vs; });
    arr.forEach(function (item, i) {
      item.el.position = { x: i * dx, y: row * dy };
      maxX = Math.max(maxX, i * dx);
    });
    row++;
  });
  var placed = {};
  nodes.forEach(function (el) {
    if (el.position) placed[el.data.id] = el.position;
  });
  var unplaced = nodes.filter(function (el) { return !el.position; });
  var pass = 0;
  while (unplaced.length && pass < 80) {
    pass++;
    var next = [];
    unplaced.forEach(function (el) {
      var id = el.data.id;
      var nbrs = adj[id] || [];
      var xs = [];
      var ys = [];
      nbrs.forEach(function (nid) {
        var p = placed[nid];
        if (p) {
          xs.push(p.x);
          ys.push(p.y);
        }
      });
      if (xs.length) {
        var cx = xs.reduce(function (a, b) { return a + b; }, 0) / xs.length;
        var cy = ys.reduce(function (a, b) { return a + b; }, 0) / ys.length;
        var salt = 0;
        for (var ci = 0; ci < id.length; ci++) salt += id.charCodeAt(ci);
        var ang = (salt % 360) * 0.01745 + pass * 0.48;
        var rad = 200 + (pass % 6) * 48 + (salt % 100);
        el.position = { x: cx + Math.cos(ang) * rad, y: cy + Math.sin(ang) * rad };
        placed[id] = el.position;
      } else {
        next.push(el);
      }
    });
    unplaced = next;
  }
  var gi = 0;
  var baseY = row * dy + 400;
  var orphanDx = 280;
  var orphanDy = 220;
  unplaced.forEach(function (el) {
    el.position = {
      x: maxX + dx * 2.2 + (gi % 8) * orphanDx,
      y: baseY + Math.floor(gi / 8) * orphanDy
    };
    gi++;
  });
  return nodes.concat(edges);
}
elements = nexusChapterLineLayout(elements);
var cy = cytoscape({
  container: document.getElementById('cy'),
  elements: elements,
  style: stylesheet,
  minZoom: 0.05,
  maxZoom: 8,
  wheelSensitivity: 0.45,
  boxSelectionEnabled: false,
  userZoomingEnabled: true,
  userPanningEnabled: true,
  motionBlur: false,
  layout: { name: 'preset', fit: true, padding: 56, animate: false }
});
(function(){
  var tip = document.createElement('div');
  tip.id = 'nexus-cy-verse-tip';
  tip.setAttribute('aria-live', 'polite');
  tip.style.cssText = 'position:fixed;z-index:100000;display:none;max-width:min(32rem,92vw);max-height:70vh;overflow:auto;padding:12px 14px;background:rgba(10,16,24,.96);border:1px solid rgba(34,211,238,.45);border-radius:12px;color:#e8eef7;box-shadow:0 12px 40px rgba(0,0,0,.55);pointer-events:none;';
  document.body.appendChild(tip);
  var refEl = document.createElement('div');
  refEl.style.cssText = 'font-family:ui-monospace,monospace;font-size:11px;color:#67e8f9;margin-bottom:8px;letter-spacing:.02em;';
  var txtEl = document.createElement('div');
  txtEl.style.cssText = 'font-family:Georgia,\"Times New Roman\",serif;font-size:14px;line-height:1.62;white-space:pre-wrap;';
  tip.appendChild(refEl);
  tip.appendChild(txtEl);
  function hideTip(){
    tip.style.display = 'none';
    refEl.textContent = '';
    txtEl.textContent = '';
  }
  function positionTip(evt){
    var oe = evt.originalEvent;
    if (!oe) return;
    var x = oe.clientX, y = oe.clientY;
    tip.style.display = 'block';
    var tw = tip.offsetWidth, th = tip.offsetHeight;
    var lx = x + 14, ly = y + 14;
    if (lx + tw > window.innerWidth - 8) lx = Math.max(8, window.innerWidth - tw - 8);
    if (ly + th > window.innerHeight - 8) ly = Math.max(8, window.innerHeight - th - 8);
    tip.style.left = lx + 'px';
    tip.style.top = ly + 'px';
  }
  cy.on('mouseover', 'node', function(evt){
    var n = evt.target;
    var ref = n.data('ref') || '';
    var vtext = n.data('verse_text');
    refEl.textContent = ref || '';
    if (vtext) txtEl.textContent = String(vtext);
    else txtEl.textContent = ref ? '(KJV text not loaded.)' : '';
    if (!ref && !vtext){ hideTip(); return; }
    positionTip(evt);
  });
  cy.on('mousemove', 'node', function(evt){
    if (tip.style.display === 'block') positionTip(evt);
  });
  cy.on('mouseout', 'node', hideTip);
  cy.on('pan zoom', hideTip);
})();
function fitGraph() { cy.fit(undefined, 56); }
document.getElementById('btn-fit').addEventListener('click', fitGraph);
document.getElementById('btn-zin').addEventListener('click', function(){
  var nz = Math.min(cy.zoom() * 1.35, cy.maxZoom());
  cy.zoom(nz);
});
document.getElementById('btn-zout').addEventListener('click', function(){
  var nz = Math.max(cy.zoom() / 1.35, cy.minZoom());
  cy.zoom(nz);
});
document.getElementById('btn-reset').addEventListener('click', function(){
  fitGraph();
  cy.center();
});
document.getElementById('btn-lines').addEventListener('click', function(){
  var flat = [];
  cy.nodes().forEach(function (n) {
    flat.push({ data: n.data(), position: n.position() });
  });
  cy.edges().forEach(function (e) {
    flat.push({ data: e.data() });
  });
  var laid = nexusChapterLineLayout(flat);
  cy.elements().remove();
  cy.add(laid);
  cy.layout({ name: 'preset', fit: true, padding: 56, animate: false }).run();
});
document.getElementById('btn-cose').addEventListener('click', function(){
  cy.layout({
    name: 'cose', animate: false, fit: true, padding: 52,
    nodeRepulsion: 4500, idealEdgeLength: 110, gravity: 0.22,
    numIter: 2200, randomize: true, componentSpacing: 80
  }).run();
});
document.getElementById('btn-png').addEventListener('click', function(){
  var png = cy.png({ output: 'blob', full: true, scale: 2, bg: '#0a1018' });
  var url = URL.createObjectURL(png);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'nexus-graph-' + new Date().toISOString().slice(0,10) + '.png';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});
document.getElementById('btn-pdf').addEventListener('click', function(){
  try {
    var imgData = cy.png({ output: 'base64uri', full: true, scale: 2, bg: '#0a1018' });
    var PDFCtor = (window.jspdf && window.jspdf.jsPDF) || window.jsPDF;
    if (!PDFCtor) { alert('PDF library not loaded — check network.'); return; }
    var doc = new PDFCtor({ orientation: 'landscape', unit: 'pt', format: 'a4' });
    var pageW = doc.internal.pageSize.getWidth();
    var pageH = doc.internal.pageSize.getHeight();
    var margin = 28;
    var maxW = pageW - 2 * margin;
    var maxH = pageH - 2 * margin;
    doc.addImage(imgData, 'PNG', margin, margin, maxW, maxH, undefined, 'FAST');
    doc.save('nexus-graph-' + new Date().toISOString().slice(0,10) + '.pdf');
  } catch (err) { console.error(err); }
});
cy.on('tap', 'node', function(evt){
  var ref = evt.target.data('ref');
  if (!ref) return;
  ref = String(ref).replace(/\\s+/g, ' ').trim();
  function assignNav(win) {
    if (!win || win.location == null) return false;
    try {
      var u = new URL(win.location.href);
      u.searchParams.set('graph_nav', ref);
      win.location.assign(u.toString());
      return true;
    } catch (err) { return false; }
  }
  if (assignNav(window.parent)) return;
  if (window.parent !== window.top && assignNav(window.top)) return;
  try {
    alert('Could not leave the graph frame to open the inspector. Use “Show group” below the graph. Reference: ' + ref);
  } catch (e2) {}
});
"""
    )
    html = (
        """<!DOCTYPE html><html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
<style>
html,body{margin:0;padding:0;background:#05080d;overflow:hidden;font-family:system-ui,sans-serif;}
#cy-toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:8px 12px;background:rgba(18,28,42,.92);border-bottom:1px solid rgba(56,189,248,.15);font:11px "JetBrains Mono",ui-monospace,monospace;color:#8b9cb3;}
#cy-toolbar button{cursor:pointer;background:rgba(34,211,238,.12);color:#e8eef7;border:1px solid rgba(34,211,238,.35);border-radius:8px;padding:5px 12px;font:inherit;letter-spacing:.04em;}
#cy-toolbar button:hover{background:rgba(167,139,250,.18);border-color:rgba(167,139,250,.45);color:#fff;}
#cy{width:100%;"""
        + f"height:{h}px;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(34,211,238,.06),transparent 55%),#0a1018;"
        + """}
.hint{margin-left:auto;font-size:10px;opacity:.88;flex:1;min-width:12rem;text-align:right;}
</style></head><body>
<div id="cy-toolbar">
<button type="button" id="btn-fit">Fit</button>
<button type="button" id="btn-zin">Zoom +</button>
<button type="button" id="btn-zout">Zoom −</button>
<button type="button" id="btn-reset">Reset</button>
<button type="button" id="btn-png" title="Download graph as PNG">PNG</button>
<button type="button" id="btn-pdf" title="Download graph as PDF">PDF</button>
<button type="button" id="btn-lines" title="Straight lines for today’s reading chapters; cross-refs orbit neighbors">Lines</button>
<button type="button" id="btn-cose" title="Organic force-directed layout">Organic</button>
<span class="hint">Hover node → KJV · Tap → reader + inspector</span>
</div>
<div id="cy"></div>
<script>"""
        + script
        + """</script></body></html>"""
    )
    components.html(html, height=h + 64, scrolling=False)


# ─────────────────────────────────────────────────────────────
# SCHEDULE HELPERS
# ─────────────────────────────────────────────────────────────
def pill_class(reading: str) -> str:
    r = reading.lower()
    if any(b.lower() in r for b in BOOKS_NT):
        return "pill-nt"
    if "psalm" in r or "proverb" in r or "ecclesiastes" in r or "song" in r:
        return "pill-psm"
    return "pill-ot"


def _normalize_schedule_reading_label(raw: str) -> str:
    """Map PDF quirks to canonical ALL_BOOKS names."""
    s = raw.strip()
    if re.match(r"^Song of Sol\.?", s, re.I):
        s = re.sub(r"^Song of Sol\.?\s*", "Song of Solomon ", s, flags=re.I)
    return s.strip()


def parse_schedule_ref(reading: str):
    """Extract (book, chapter) from GVCC strings: 'Leviticus 22', 'Genesis 1-2', 'Psalms 119:1-24', 'Obadiah'."""
    s = _normalize_schedule_reading_label(reading)
    if not s:
        return None, None

    # Chapter:verse range → use chapter only
    m = re.match(r"^(.+?)\s+(\d+)\s*:\s*\d", s)
    if m:
        book = m.group(1).strip()
        ch = int(m.group(2))
        if book in ALL_BOOKS:
            return book, ch

    # Book N or Book N-M (first chapter)
    m = re.match(r"^(.+?)\s+(\d+)(?:\s*-\s*\d+)?\s*$", s)
    if m:
        book = m.group(1).strip()
        ch = int(m.group(2))
        if book in ALL_BOOKS:
            return book, ch

    # Single-chapter books listed alone (Obadiah, Philemon, Jude, 2 John, 3 John)
    if s in ALL_BOOKS and CHAPTERS_PER_BOOK.get(s, 0) == 1:
        return s, 1

    return None, None


def expand_schedule_reading_chapters(reading: str) -> list[tuple[str, int]]:
    """All (book, chapter) pairs covered by one GVCC schedule line (handles e.g. Genesis 1-2)."""
    s = _normalize_schedule_reading_label(reading)
    if not s:
        return []

    m = re.match(r"^(.+?)\s+(\d+)\s*:\s*\d", s)
    if m:
        book, ch = m.group(1).strip(), int(m.group(2))
        return [(book, ch)] if book in ALL_BOOKS else []

    m = re.match(r"^(.+?)\s+(\d+)\s*-\s*(\d+)\s*$", s)
    if m:
        book, c1, c2 = m.group(1).strip(), int(m.group(2)), int(m.group(3))
        if book not in ALL_BOOKS:
            return []
        max_c = CHAPTERS_PER_BOOK.get(book, c2)
        hi = min(c2, max_c)
        lo = max(1, min(c1, hi))
        return [(book, c) for c in range(lo, hi + 1)]

    m = re.match(r"^(.+?)\s+(\d+)\s*$", s)
    if m:
        book, ch = m.group(1).strip(), int(m.group(2))
        return [(book, ch)] if book in ALL_BOOKS else []

    if s in ALL_BOOKS and CHAPTERS_PER_BOOK.get(s, 0) == 1:
        return [(s, 1)]

    return []


@st.cache_data(ttl=86400, show_spinner=False)
def _schedule_chapter_keys_for_calendar_day(month: int, day: int) -> tuple[str, ...]:
    """Cached by calendar date; recomputes at most once per (month, day) per process."""
    seen: set[str] = set()
    out: list[str] = []
    for label in sched.get_readings(month, day):
        for book, ch in expand_schedule_reading_chapters(label):
            k = f"{book}|{ch}"
            if k not in seen:
                seen.add(k)
                out.append(k)
    return tuple(sorted(out))


def today_schedule_chapter_keys() -> list[str]:
    """Stable list of 'Book|chapter' keys for today's plan (for graph line layout)."""
    t = date.today()
    return list(_schedule_chapter_keys_for_calendar_day(t.month, t.day))


@st.cache_data(ttl=3600, show_spinner=False)
def _warm_schedule_chapters(_readings_key: tuple[str, ...]) -> None:
    """Pre-fetch today's schedule chapters so buttons feel instant."""
    for label in _readings_key:
        for book, ch in expand_schedule_reading_chapters(label):
            if book and ch:
                fetch_chapter(book, ch)


def render_reader_verse_notes() -> None:
    """In-reader notes for the active verse (same file as sidebar: verse_notes.json)."""
    with st.expander("✎ Notes for selected verse", expanded=False):
        av = st.session_state.active_verse
        if not av:
            st.caption(
                "Click a verse in this chapter, or tap a node in the graph, to choose a verse for notes."
            )
            return
        nid = clean_ref(av)
        vnotes = load_verse_notes()
        ta_key = f"reader_vnote_{nid}"
        sk = f"sidebar_vnote_{nid}"
        if ta_key not in st.session_state:
            st.session_state[ta_key] = vnotes.get(nid, {}).get("text", "")
        st.caption(f"Stored with sidebar notes · {av}")
        st.text_area(
            "Write notes",
            key=ta_key,
            height=140,
            placeholder="Your thoughts on this verse…",
            label_visibility="collapsed",
        )
        if st.button("Save note", key=f"reader_bsave_v_{nid}", use_container_width=True):
            t = str(st.session_state.get(ta_key, ""))
            vnotes[nid] = {
                "text": t,
                "verse_ref": av,
                "updated": datetime.now().isoformat(timespec="seconds"),
            }
            save_verse_notes(vnotes)
            st.session_state[sk] = t
            st.session_state.status_msg = "Verse note saved."
            st.session_state.status_type = "success"
            st.rerun()


def render_bible_reader(reader_hover_inspector: bool = False):
    """Book/chapter controls, click-to-select verses, TSK strip."""
    st.markdown('<div class="panel-title">📖 Bible Reader</div>', unsafe_allow_html=True)

    if st.session_state.book not in ALL_BOOKS:
        st.session_state.book = ALL_BOOKS[0]

    c1, c2 = st.columns([3, 1])
    with c1:
        st.selectbox("Book", ALL_BOOKS, key="book", label_visibility="collapsed")
    max_ch = CHAPTERS_PER_BOOK.get(st.session_state.book, 150)
    if st.session_state.chapter > max_ch:
        st.session_state.chapter = max_ch
    if st.session_state.chapter < 1:
        st.session_state.chapter = 1
    with c2:
        st.number_input(
            "Ch", min_value=1, max_value=max_ch,
            key="chapter", label_visibility="collapsed"
        )

    loc = (st.session_state.book, int(st.session_state.chapter))
    ploc = st.session_state.get("_reader_loc")
    if ploc is not None and ploc != loc:
        st.session_state.chapter_verses = []
        st.session_state.selected_verse_num = None
    st.session_state._reader_loc = loc

    sel_book = st.session_state.book
    sel_ch = int(st.session_state.chapter)

    if not st.session_state.chapter_verses:
        st.session_state.chapter_verses = fetch_chapter(sel_book, sel_ch)

    verses = st.session_state.chapter_verses

    if verses:
        st.markdown(
            '<p class="verse-click-hint">Click a verse below — it becomes active, joins the brain, '
            "and links automatically to the previous active verse.</p>",
            unsafe_allow_html=True,
        )

        if st.button(
            "⛓ Linear / snake chain · this chapter",
            key=f"linear_snake_{sel_book}_{sel_ch}",
            use_container_width=True,
            help=(
                "Add every verse in this chapter to the graph and link them in order: "
                "v1 → v2 → v3 → … (one directed chain). "
                "Skips links that already exist."
            ),
        ):
            n_v, n_new, e_new = build_linear_chapter_chain(sel_book, sel_ch, verses)
            st.session_state.status_msg = (
                f"Snake chain: {n_v} verses in sequence "
                f"({n_new} new nodes, {e_new} new edges)."
            )
            st.session_state.status_type = "success"
            st.rerun()

        if len(verses) <= 56:
            for v in verses:
                vn, txt = v["verse"], v["text"]
                ref = f"{sel_book} {sel_ch}:{vn}"
                is_act = st.session_state.active_verse == ref
                short = txt if len(txt) <= 160 else txt[:157] + "…"
                label = f"{'⬤ ' if is_act else ''}{vn}  {short}"
                if st.button(label, key=f"vrow_{sel_book}_{sel_ch}_{vn}", use_container_width=True):
                    prev = st.session_state.active_verse
                    add_node(ref)
                    st.session_state.active_verse = ref
                    st.session_state.selected_verse_num = vn
                    if prev and clean_ref(prev) != clean_ref(ref):
                        add_edge(prev, ref)
                    sync_split_inspector_content_from_reader_ref(ref)
                    st.rerun()
        else:
            st.caption("Many verses — use number grid, then read the chapter below.")
            ngrid = 12
            for row_start in range(0, len(verses), ngrid):
                row = verses[row_start: row_start + ngrid]
                cols = st.columns(len(row))
                for col, v in zip(cols, row):
                    vn = v["verse"]
                    ref = f"{sel_book} {sel_ch}:{vn}"
                    with col:
                        if st.button(str(vn), key=f"vnum_{sel_book}_{sel_ch}_{vn}", use_container_width=True):
                            prev = st.session_state.active_verse
                            add_node(ref)
                            st.session_state.active_verse = ref
                            st.session_state.selected_verse_num = vn
                            if prev and clean_ref(prev) != clean_ref(ref):
                                add_edge(prev, ref)
                            sync_split_inspector_content_from_reader_ref(ref)
                            st.rerun()

        st.markdown("---")
        html_lines = []
        for v in verses:
            vn = v["verse"]
            txt = v["text"]
            cls = "active-verse-highlight" if vn == st.session_state.selected_verse_num else ""
            ref = f"{sel_book} {sel_ch}:{vn}"
            ref_attr = html_module.escape(ref, quote=True)
            html_lines.append(
                f'<span class="{cls}" id="v{vn}" data-verse-num="{vn}" data-nexus-ref="{ref_attr}">'
                f'<sup class="verse-num">{vn}</sup>{txt} '
                f"</span>"
            )
        st.markdown(
            f'<div class="bible-text">{"".join(html_lines)}</div>',
            unsafe_allow_html=True,
        )

        if reader_hover_inspector:
            components.html(
                r"""
<script>
(function () {
  var rootWin;
  try {
    rootWin = window.top && window.top.location ? window.top : window.parent;
  } catch (e) {
    rootWin = window.parent;
  }
  var doc = rootWin.document;
  var timer = null;
  var lastRef = null;
  function go(ref) {
    if (!ref || ref === lastRef) return;
    lastRef = ref;
    try {
      var u = new URL(rootWin.location.href);
      u.searchParams.set('reader_inspector', ref);
      rootWin.location.assign(u.toString());
    } catch (e) {}
  }
  function refFromEvent(ev) {
    var el = ev.target && ev.target.closest && ev.target.closest('[data-nexus-ref]');
    if (!el) return null;
    return el.getAttribute('data-nexus-ref');
  }
  doc.addEventListener('click', function (ev) {
    var ref = refFromEvent(ev);
    if (!ref) return;
    clearTimeout(timer);
    timer = null;
    go(ref);
  }, true);
  doc.addEventListener('mouseover', function (ev) {
    var ref = refFromEvent(ev);
    if (!ref) return;
    clearTimeout(timer);
    timer = setTimeout(function () { go(ref); }, 450);
  }, true);
})();
</script>
""",
                height=0,
            )

        scroll_vs = st.session_state.pop("_scroll_verse_num", None)
        if scroll_vs is not None:
            v_js = int(scroll_vs)
            components.html(
                f"""<script>
(function() {{
  var vs = {v_js};
  function scrollToVerse() {{
    try {{
      var doc = window.parent.document;
      var root = doc.querySelector('[data-testid="stAppViewContainer"]') || doc.body;
      var wrap = root.querySelector(".bible-text") || root;
      var el = wrap.querySelector('[data-verse-num="' + vs + '"]');
      if (el) el.scrollIntoView({{behavior: "smooth", block: "center"}});
    }} catch (e) {{}}
  }}
  setTimeout(scrollToVerse, 250);
  setTimeout(scrollToVerse, 700);
}})();
</script>""",
                height=1,
            )

        av = st.session_state.active_verse
        if av:
            tsk_rows = top_tsk_related(av, limit=6)
            seed = sched.CROSS_REFERENCES.get(av, [])
            if tsk_rows or seed:
                st.markdown('<div class="tsk-inline-row"></div>', unsafe_allow_html=True)
                st.caption("Recommended cross-references (TSK + seed) — click to link to active verse:")
                if seed:
                    scols = st.columns(min(4, max(1, len(seed))))
                    for i, xref in enumerate(seed[:6]):
                        with scols[i % len(scols)]:
                            if st.button(
                                xref,
                                key=f"seed_in_{clean_ref(av)}_{i}",
                                use_container_width=True,
                                type="secondary",
                                help=xref_preview_tooltip(xref),
                            ):
                                link_crossref_to_active(av, xref, note="seed")
                if tsk_rows:
                    tcols = st.columns(min(3, len(tsk_rows)))
                    for i, (disp, wt) in enumerate(tsk_rows):
                        with tcols[i % len(tcols)]:
                            if st.button(
                                f"{disp}  ·{wt}",
                                key=f"tsk_in_{clean_ref(av)}_{i}",
                                use_container_width=True,
                                type="secondary",
                                help=xref_preview_tooltip(disp),
                            ):
                                link_crossref_to_active(av, disp, note="TSK")
    else:
        _has_local = _kjv_local_mtime() > 0
        st.warning(
            "**Could not load this chapter.** This is not always a “no internet” problem.\n\n"
            "- **bible-api.com** rate-limits (~15 requests per 30s per IP). Opening many chapters quickly can hit the limit — wait a few seconds and use **Retry** below.\n"
            "- **Stale cache:** a past failed fetch may be cached — **Retry** clears it.\n"
            + (
                "- **Local file:** `kjv_by_chapter.json` is present but this book/chapter may be missing or malformed — fix the file or remove it to use the API.\n"
                if _has_local
                else "- **Tip:** Download **local KJV** in the sidebar once for reliable offline chapters.\n"
            )
        )
        if st.button(
            "Retry loading chapter",
            key=f"retry_ch_{sel_book}_{sel_ch}",
            use_container_width=True,
        ):
            try:
                fetch_chapter.clear()
            except Exception:
                pass
            st.session_state.chapter_verses = []
            st.rerun()

    render_reader_verse_notes()


def render_graph_text_inspector_panel(*, compact_close: bool = False) -> None:
    """Full 1-hop text inspector + Show group (used in Split right column or Brain under graph)."""
    st.markdown('<div id="split-inspector-anchor"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📋 Graph text inspector</div>', unsafe_allow_html=True)
    st.caption(
        "Verses **one graph edge away** from the focus verse, with full KJV. "
        "Focus comes from a **graph tap**, **Show group**, or **click / hover** the scripture text on the left (Split view)."
    )
    ref = st.session_state.get("_graph_node_panel_ref")
    if compact_close:
        c1, c2 = st.columns([5, 1])
        with c1:
            if ref:
                st.markdown(f"**Focus:** `{html_module.escape(ref)}`", unsafe_allow_html=True)
        with c2:
            if ref and st.button("Close", key="split_insp_close_btn", use_container_width=True):
                st.session_state.pop("_graph_node_panel_ref", None)
                st.session_state["graph_inspector_manual_pick"] = GRAPH_INSPECTOR_PICK_PLACEHOLDER
                st.rerun()
    else:
        if ref and st.button("Close inspector", key="split_insp_close_wide", use_container_width=True):
            st.session_state.pop("_graph_node_panel_ref", None)
            st.session_state["graph_inspector_manual_pick"] = GRAPH_INSPECTOR_PICK_PLACEHOLDER
            st.rerun()

    if ref:
        _render_graph_node_panel_body(ref)
    else:
        st.info(
            "No focus verse yet — **click or hover** any verse in the Bible text on the left (Split), "
            "or switch to **🧠 Graph** and tap a node."
        )

    _uniq = sorted(
        {n["data"]["ref"] for n in st.session_state.nodes if n.get("data", {}).get("ref")}
    )
    if _uniq:
        st.caption("Pick any graph verse and load its 1-hop group here (also jumps the reader).")
        _gpick = st.selectbox(
            "Verse for text inspector",
            options=[GRAPH_INSPECTOR_PICK_PLACEHOLDER] + _uniq,
            key="graph_inspector_manual_pick",
            label_visibility="collapsed",
        )
        if st.button("Show group", key="graph_inspector_manual_btn"):
            if not _gpick or _gpick == GRAPH_INSPECTOR_PICK_PLACEHOLDER:
                st.warning("Choose a verse in the dropdown first.")
            else:
                st.session_state["_pending_open_graph_group"] = _gpick
                st.rerun()


def render_graph_and_search_panels(
    graph_height: int = 400,
    collapse_bottom: bool = False,
    *,
    split_right_focus: str | None = None,
):
    """Cytoscape + schedule/search, or inspector-only when split_right_focus=='inspector'."""
    st.markdown('<div id="brain-graph-anchor"></div>', unsafe_allow_html=True)

    if split_right_focus == "inspector":
        render_graph_text_inspector_panel(compact_close=True)
    else:
        st.markdown('<div class="panel-title">🧠 Brain Connections</div>', unsafe_allow_html=True)
        st.caption(
            "Put the pointer **inside** the graph frame, then **scroll** to zoom (trackpad or mouse wheel). "
            "Use **Fit / Zoom ±** if scroll is captured by the page. **PNG / PDF** saves the current layout. "
            "**Node colors:** emerald = memorized, slate = not memorized, cyan = NT unset, amber = OT unset. "
            "Default **Lines** layout: only **today’s reading** chapters are straight chains (v1→v2→…); "
            "other linked verses sit **near** what they connect to. **Organic** = full force layout. "
            "Each persist updates `brain_by_day/`; midnight archive in sidebar."
        )

        elements = cytoscape_elements_with_hover_text()

        if elements:
            render_brain_graph_interactive(elements, CYTOSCAPE_STYLESHEET, graph_height)

            _uniq = sorted(
                {n["data"]["ref"] for n in st.session_state.nodes if n.get("data", {}).get("ref")}
            )
            if _uniq and split_right_focus is None:
                st.caption(
                    "**Text inspector:** tap a node in the graph, or choose a verse below and click **Show group**."
                )
                _gpick = st.selectbox(
                    "Verse for text inspector",
                    options=[GRAPH_INSPECTOR_PICK_PLACEHOLDER] + _uniq,
                    key="graph_inspector_manual_pick",
                    label_visibility="collapsed",
                )
                if st.button("Show group", key="graph_inspector_manual_btn"):
                    if not _gpick or _gpick == GRAPH_INSPECTOR_PICK_PLACEHOLDER:
                        st.warning("Choose a verse in the dropdown first.")
                    else:
                        st.session_state["_pending_open_graph_group"] = _gpick
                        st.rerun()

            with st.expander("Manage nodes", expanded=False):
                node_refs = [n["data"]["ref"] for n in st.session_state.nodes]
                if node_refs:
                    del_ref = st.selectbox("Remove node", node_refs, key="del_sel")
                    if st.button("🗑 Remove", key="btn_del"):
                        remove_node(del_ref)
                        st.session_state.status_msg = f"Removed {del_ref}"
                        st.session_state.status_type = "info"
                        st.rerun()
                else:
                    st.caption("No nodes yet — click verses in the reader.")
        else:
            st.markdown(
                '<div style="text-align:center;padding:2.5rem;color:#7070a0;font-size:.85rem;">'
                "Your brain graph appears here.<br>"
                "<b>Click any verse</b> in the reader to seed the network."
                "</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin:.5rem 0'></div>", unsafe_allow_html=True)

    _bottom = (
        st.expander("📅 Schedule · 🔍 Search & cross-references", expanded=False)
        if collapse_bottom
        else st.container()
    )
    with _bottom:
        sched_col, search_col = st.columns(2, gap="medium")
        _render_schedule_search_columns(sched_col, search_col)


def _render_schedule_search_columns(sched_col, search_col) -> None:
    today_local = date.today()

    with sched_col:
        st.markdown('<div class="panel-title">📅 Today\'s Readings</div>', unsafe_allow_html=True)
        readings = sched.get_today_readings()

        if readings:
            pills_html = ""
            for r in readings:
                pc = pill_class(r)
                pills_html += f'<span class="sched-pill {pc}">{r}</span>'
            st.markdown(pills_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            for i, r in enumerate(readings):
                st.button(
                    f"📖 {r}",
                    key=f"sched_today_{i}",
                    on_click=_on_schedule_reading_click,
                    args=(r,),
                    use_container_width=True,
                )

            st.markdown("---")

            if st.button("⬤ Seed Graph w/ Today", key="btn_seed", use_container_width=True):
                for r in readings:
                    book_name, ch_num = parse_schedule_ref(r)
                    if book_name and ch_num:
                        ref = f"{book_name} {ch_num}:1"
                        add_node(ref)
                st.session_state.status_msg = "Seeded graph with today's readings"
                st.session_state.status_type = "success"
                st.rerun()

            if st.button(
                "📎 Top 10 TSK · today’s reading chapters",
                key="btn_tsk_today_schedule_chain",
                use_container_width=True,
                help=(
                    "For every verse **already on the graph** in **today’s schedule chapters** "
                    "(the same chapters that get the straight line / snake layout in the graph), "
                    "add up to 10 local TSK cross-references each: new nodes and links. "
                    "Requires normalized_edges.csv."
                ),
            ):
                sch_n, nn, ee = link_top_tsk_for_today_schedule_nodes(limit=10)
                if sch_n < 0:
                    st.session_state.status_msg = (
                        "TSK batch skipped — no edge file found (add **normalized_edges.csv** beside the app)."
                    )
                    st.session_state.status_type = "warning"
                elif sch_n == 0:
                    st.session_state.status_msg = (
                        "No graph nodes in today’s schedule chapters yet — add verses from those chapters "
                        "(e.g. snake chain) or check today’s plan."
                    )
                    st.session_state.status_type = "warning"
                elif nn == 0 and ee == 0:
                    st.session_state.status_msg = (
                        f"TSK: {sch_n} verse(s) in today’s chapters — nothing new to add (already linked or no TSK rows)."
                    )
                    st.session_state.status_type = "info"
                else:
                    st.session_state.status_msg = (
                        f"TSK batch: {sch_n} verse(s) in today’s chapters → {nn} new nodes, {ee} new edges."
                    )
                    st.session_state.status_type = "success"
                st.rerun()
        else:
            st.caption(f"No schedule entry for {today_local.strftime('%B')} {today_local.day}.")

        av = st.session_state.active_verse
        if av and av in sched.CROSS_REFERENCES:
            st.markdown("**Suggested cross-references:**", unsafe_allow_html=False)
            for xref in sched.CROSS_REFERENCES[av]:
                tip = html_module.escape(xref_preview_tooltip(xref)[:480])
                xsafe = html_module.escape(xref)
                st.markdown(
                    f'<span class="sched-pill pill-nt" title="{tip}">{xsafe}</span>',
                    unsafe_allow_html=True,
                )

    with search_col:
        st.markdown('<div class="panel-title">🔍 Cross-Reference & Search</div>', unsafe_allow_html=True)

        av = st.session_state.active_verse
        if av:
            st.markdown(
                f'<div class="node-info">Active verse: <span>{av}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="node-info" style="color:#7070a0">No active verse — click a verse in the reader</div>',
                unsafe_allow_html=True,
            )

        search_ref = st.text_input(
            "Search verse / passage",
            value=st.session_state.search_ref,
            placeholder="e.g.  Romans 8:28  or  Psalm 23:1",
            key="search_input",
            label_visibility="collapsed",
        )
        st.session_state.search_ref = search_ref

        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("🔍 Fetch", key="btn_fetch", use_container_width=True):
                if search_ref.strip():
                    with st.spinner("Fetching…"):
                        result = fetch_verse(search_ref.strip())
                    st.session_state.search_result = result
                    if not result:
                        st.session_state.status_msg = f"Could not find: {search_ref}"
                        st.session_state.status_type = "warning"
                else:
                    st.session_state.status_msg = "Enter a reference first"
                    st.session_state.status_type = "warning"

        with sc2:
            can_link = st.session_state.active_verse and st.session_state.search_result
            if st.button(
                "🔗 Link to Active", key="btn_link",
                use_container_width=True,
                disabled=not can_link,
            ):
                sr = st.session_state.search_result
                ref = sr["reference"]
                add_node_and_maybe_link(ref)
                add_node(st.session_state.active_verse)
                add_edge(st.session_state.active_verse, ref)
                st.session_state.status_msg = f"Linked {st.session_state.active_verse} ↔ {ref}"
                st.session_state.status_type = "success"
                st.rerun()

        if st.session_state.search_result:
            sr = st.session_state.search_result
            st.markdown(
                f'<div class="node-info" style="margin-top:.5rem">'
                f'<span>{sr["reference"]}</span><br>'
                f'<span style="color:#dcdcf0;font-family:\'Crimson Text\',serif;font-size:.95rem;font-weight:400">'
                f'{sr["text"]}'
                f"</span></div>",
                unsafe_allow_html=True,
            )

            sa, sb = st.columns(2)
            with sa:
                if st.button("＋ Add to Graph", key="btn_add_sr", use_container_width=True):
                    add_node_and_maybe_link(sr["reference"])
                    if st.session_state.auto_link_to_active and st.session_state.active_verse and st.session_state.active_verse != sr["reference"]:
                        st.session_state.status_msg = f"Added + linked {sr['reference']}"
                    else:
                        st.session_state.status_msg = f"Added {sr['reference']}"
                    st.session_state.status_type = "info"
                    st.rerun()
            with sb:
                if st.button("📖 Open in Reader", key="btn_open_sr", use_container_width=True):
                    m = re.match(r"^(.+?)\s+(\d+):(\d+)", sr["reference"])
                    if m:
                        b, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
                        if b in ALL_BOOKS:
                            st.session_state.book = b
                            st.session_state.chapter = ch
                            st.session_state.selected_verse_num = vs
                            st.session_state.chapter_verses = []
                            st.session_state._reader_loc = (b, ch)
                            st.rerun()

        st.markdown("---")

        av2 = st.session_state.active_verse
        if av2 and av2 in sched.CROSS_REFERENCES:
            st.caption("Quick-link suggestions:")
            for xref in sched.CROSS_REFERENCES[av2]:
                if st.button(
                    f"🔗 {xref}",
                    key=f"xr_{clean_ref(av2)}_{clean_ref(xref)}",
                    use_container_width=True,
                    type="secondary",
                    help=xref_preview_tooltip(xref),
                ):
                    result = fetch_verse(xref)
                    if result:
                        add_node(av2)
                        add_node_and_maybe_link(result["reference"])
                        add_edge(av2, result["reference"])
                        st.session_state.status_msg = f"Linked {av2} ↔ {result['reference']}"
                        st.session_state.status_type = "success"
                    st.rerun()

        if av2:
            tsk_related = top_tsk_related(av2, limit=10)
            if tsk_related:
                st.caption("TSK / local cross-reference suggestions:")
                for ref, wt in tsk_related:
                    if st.button(
                        f"🔗 {ref} (w={wt})",
                        key=f"tsk_{clean_ref(av2)}_{clean_ref(ref)}",
                        use_container_width=True,
                        type="secondary",
                        help=xref_preview_tooltip(ref),
                    ):
                        result = fetch_verse(ref)
                        if result:
                            add_node(av2)
                            add_node_and_maybe_link(result["reference"])
                            add_edge(av2, result["reference"])
                            st.session_state.status_msg = f"Linked {av2} ↔ {result['reference']} (TSK)"
                            st.session_state.status_type = "success"
                        else:
                            add_node(av2)
                            add_node_and_maybe_link(ref)
                            add_edge(av2, ref)
                            st.session_state.status_msg = f"Linked {av2} ↔ {ref} (TSK, unresolved text)"
                            st.session_state.status_type = "info"
                        st.rerun()


def render_notes_sidebar() -> None:
    """Persistent notes: per-verse + per edge (two connected nodes in the graph)."""
    st.markdown("#### Verse & link notes")
    st.caption(
        "Saved to `verse_notes.json` and `edge_notes.json` in this folder. "
        "Click a graph node or a verse in the reader to set the active verse."
    )
    av = st.session_state.active_verse
    if not av:
        st.info("No active verse — open one from the reader or by tapping a node in the graph.")
        return

    nid_m = clean_ref(av)
    vm = st.session_state.verse_memorization
    cur_lab = (
        "Memorized"
        if vm.get(nid_m) is True
        else "Not memorized"
        if vm.get(nid_m) is False
        else "(not set)"
    )
    labels = ["(not set)", "Memorized", "Not memorized"]
    ix = labels.index(cur_lab)
    choice = st.selectbox(
        "Verse memory (colors graph)",
        labels,
        index=ix,
        key=f"mempick_{nid_m}",
        help="Emerald node = memorized · slate = not memorized · cyan/amber = not set (NT/OT).",
    )
    if choice != cur_lab:
        if choice == "(not set)":
            vm.pop(nid_m, None)
        elif choice == "Memorized":
            vm[nid_m] = True
        else:
            vm[nid_m] = False
        save_memorization_file(vm)
        sync_node_colors_in_session()
        _persist()
        st.rerun()

    vnotes = load_verse_notes()
    nid = clean_ref(av)
    ta_key = f"sidebar_vnote_{nid}"
    if ta_key not in st.session_state:
        st.session_state[ta_key] = vnotes.get(nid, {}).get("text", "")

    st.text_area(f"Note for {av}", height=140, key=ta_key, placeholder="Your thoughts on this verse…")
    if st.button("Save verse note", key=f"bsave_v_{nid}"):
        t = str(st.session_state.get(ta_key, ""))
        vnotes[nid] = {
            "text": t,
            "verse_ref": av,
            "updated": datetime.now().isoformat(timespec="seconds"),
        }
        save_verse_notes(vnotes)
        st.session_state.status_msg = "Verse note saved."
        st.session_state.status_type = "success"
        st.rerun()

    nbrs = neighbor_refs_for(av)
    if nbrs:
        st.markdown("**Connection note** (for one edge in the graph)")
        pick = st.selectbox("Other verse in this link", nbrs, key=f"nbr_pick_{nid}")
        ek = canonical_edge_key(av, pick)
        enotes = load_edge_notes()
        ek_key = f"sidebar_enote_{ek}"
        if ek_key not in st.session_state:
            st.session_state[ek_key] = enotes.get(ek, {}).get("text", "")
        st.text_area(
            f"Why {av} ↔ {pick}?",
            height=110,
            key=ek_key,
            placeholder="How these verses connect for you…",
        )
        if st.button("Save link note", key=f"bsave_e_{ek}"):
            t2 = str(st.session_state.get(ek_key, ""))
            enotes[ek] = {
                "text": t2,
                "a": av,
                "b": pick,
                "updated": datetime.now().isoformat(timespec="seconds"),
            }
            save_edge_notes(enotes)
            st.session_state.status_msg = "Connection note saved."
            st.session_state.status_type = "success"
            st.rerun()
    else:
        st.caption("Add edges in the graph (link verses) to write notes for specific connections.")


def _render_graph_node_panel_body(ref: str) -> None:
    """Every verse in the 1-hop group (tapped + all neighbors): full KJV, one list."""
    ref = re.sub(r"\s+", " ", (ref or "").strip())
    if not ref:
        return
    group = one_hop_group_refs(ref)
    if len(group) == 1:
        st.caption("Only this node — no edges yet. Add links in the graph to grow this group.")
    else:
        st.caption(
            f"{len(group)} passages — the node you opened plus every verse **one edge away** in your graph."
        )
    for idx, r in enumerate(group):
        if idx:
            st.divider()
        tag = " — tapped" if idx == 0 else " — linked (1 hop)"
        st.markdown(f"#### {html_module.escape(r)}{tag}")
        d = fetch_verse(r)
        if d:
            st.markdown(
                '<div class="node-info" style="margin-top:0.35rem">'
                '<span style="font-family:Georgia,\'Times New Roman\',serif;font-size:1.05rem;line-height:1.72">'
                f"{html_module.escape(d['text'])}</span></div>",
                unsafe_allow_html=True,
            )
        else:
            st.warning("Could not load Bible text for this reference (tried KJV, WEB, and chapter cache).")


# ─────────────────────────────────────────────────────────────
# APP HEADER
# ─────────────────────────────────────────────────────────────
today = date.today()
today_str = f"{today.strftime('%A, %B')} {today.day} {today.year}"
active_label = f"Active: {st.session_state.active_verse}" if st.session_state.active_verse else "No active verse"

st.markdown(f"""
<div class="app-header">
  <div class="app-header-brand">
    <h1>NEXUS</h1>
    <span class="app-header-tagline">Scripture graph · Zettelkasten</span>
  </div>
  <span class="date-pill">◷ {today_str}</span>
  <span class="active-pill">◇ {active_label}</span>
  <a class="graph-focus-link" href="#brain-graph-anchor" title="Scroll to brain graph">GRAPH ↗</a>
  <span class="stat-pill">
    {len(st.session_state.nodes)} nodes · {len(st.session_state.edges)} edges
  </span>
</div>
""", unsafe_allow_html=True)

_gpanel_ref = st.session_state.get("_graph_node_panel_ref")
_view_for_header = st.session_state.get("view_mode", "Split")
if _gpanel_ref and _view_for_header != "Split":
    st.markdown(
        '<div id="graph-inspector-anchor" class="graph-inspector-anchor"></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        ih1, ih2 = st.columns([4, 1])
        with ih1:
            st.markdown("#### ◇ Graph text inspector")
            st.caption(
                "In **Split** view the inspector lives in the **right column** (📋 Text inspector). "
                "Here: tapped verse plus **1-hop** neighbors with KJV."
            )
        with ih2:
            if st.button("Close panel", use_container_width=True, key="graph_inspector_close"):
                st.session_state.pop("_graph_node_panel_ref", None)
                st.session_state["graph_inspector_manual_pick"] = GRAPH_INSPECTOR_PICK_PLACEHOLDER
                st.rerun()
        _render_graph_node_panel_body(_gpanel_ref)

# ─────────────────────────────────────────────────────────────
# MAIN LAYOUT  (Split | Reader-only | Brain-focused)
# ─────────────────────────────────────────────────────────────
with st.container(border=True):
    vt_a, vt_b = st.columns([1, 6])
    with vt_a:
        st.markdown('<span class="view-label">Layout</span>', unsafe_allow_html=True)
    with vt_b:
        st.radio(
            "View",
            ["Split", "Reader", "Brain"],
            horizontal=True,
            key="view_mode",
            label_visibility="collapsed",
        )

_today_readings = sched.get_today_readings()
if _today_readings:
    _warm_sig = (date.today().isoformat(), tuple(_today_readings))
    if st.session_state.get("_schedule_prefetch_key") != _warm_sig:
        _warm_schedule_chapters(tuple(_today_readings))
        st.session_state["_schedule_prefetch_key"] = _warm_sig

_mode = st.session_state.get("view_mode", "Split")
if _mode == "Reader":
    render_bible_reader()
elif _mode == "Brain":
    render_graph_and_search_panels(graph_height=620, collapse_bottom=True)
else:
    st.markdown(
        '<div id="nexus-split-scroll-marker" aria-hidden="true" '
        'style="display:none;width:0;height:0;overflow:hidden"></div>',
        unsafe_allow_html=True,
    )
    _lc, _rc = st.columns([44, 56], gap="medium")
    with _lc:
        render_bible_reader(reader_hover_inspector=True)
    with _rc:
        st.markdown('<span class="view-label">Right column</span>', unsafe_allow_html=True)
        st.caption(
            "**Graph** vs **Text inspector**: your toggle below chooses the pane; verse picks on the left still update the inspector focus in the background."
        )
        st.radio(
            "Right panel",
            ["graph", "inspector"],
            horizontal=True,
            key="split_right_panel",
            format_func=lambda x: "🧠 Graph" if x == "graph" else "📋 Text inspector",
            label_visibility="collapsed",
            on_change=_persist_split_right_panel_to_meta,
        )
        _split_focus = st.session_state.get("split_right_panel", "graph")
        if _split_focus == "graph":
            render_graph_and_search_panels(
                graph_height=480, collapse_bottom=False, split_right_focus="graph"
            )
        else:
            render_graph_and_search_panels(
                graph_height=480, collapse_bottom=False, split_right_focus="inspector"
            )
    components.html(
        """
<script>
(function () {
  var w = window.parent;
  var doc = w.document;
  function columnAncestors(el) {
    var n = 0;
    var p = el;
    while (p) {
      if (p.getAttribute && p.getAttribute("data-testid") === "column") n++;
      p = p.parentElement;
    }
    return n;
  }
  function clearPanes() {
    doc.querySelectorAll('[data-nexus-split-pane="1"]').forEach(function (el) {
      el.removeAttribute("data-nexus-split-pane");
      el.style.maxHeight = "";
      el.style.height = "";
      el.style.overflowY = "";
      el.style.overflowX = "";
      el.style.minHeight = "";
      el.style.alignSelf = "";
    });
  }
  w.__nexusSplitReflow = function () {
    try {
      clearPanes();
      if (!doc.getElementById("nexus-split-scroll-marker")) return;
      var main = doc.querySelector("section.main") || doc.body;
      var blocks = main.querySelectorAll('[data-testid="stHorizontalBlock"]');
      var i, hb, cols, j, c, h, top;
      for (i = 0; i < blocks.length; i++) {
        hb = blocks[i];
        if (columnAncestors(hb) !== 0) continue;
        cols = hb.querySelectorAll(':scope > [data-testid="column"]');
        if (cols.length !== 2) continue;
        if (cols[0].getBoundingClientRect().width < 120) continue;
        if (cols[1].getBoundingClientRect().width < 120) continue;
        if (hb.parentElement) hb.parentElement.style.alignItems = "flex-start";
        for (j = 0; j < cols.length; j++) {
          c = cols[j];
          top = c.getBoundingClientRect().top;
          h = Math.max(200, w.innerHeight - top - 20);
          c.setAttribute("data-nexus-split-pane", "1");
          c.style.boxSizing = "border-box";
          c.style.maxHeight = h + "px";
          c.style.height = h + "px";
          c.style.overflowY = "auto";
          c.style.overflowX = "hidden";
          c.style.minHeight = "0";
          c.style.alignSelf = "flex-start";
        }
        return;
      }
    } catch (e) {}
  };
  if (!w.__nexusSplitScrollInit) {
    w.__nexusSplitScrollInit = true;
    w.addEventListener("resize", function () {
      if (w.__nexusSplitReflow) w.__nexusSplitReflow();
    });
    if (w.ResizeObserver) {
      new w.ResizeObserver(function () {
        if (w.__nexusSplitReflow) w.__nexusSplitReflow();
      }).observe(doc.documentElement);
    }
  }
  var rf = w.__nexusSplitReflow;
  rf();
  setTimeout(rf, 50);
  setTimeout(rf, 200);
  setTimeout(rf, 500);
  setTimeout(rf, 1200);
})();
</script>
""",
        height=0,
    )

# ─────────────────────────────────────────────────────────────
# STATUS BAR
# ─────────────────────────────────────────────────────────────
_rollover = st.session_state.pop("_graph_rollover_notice", None)
if _rollover:
    st.info(_rollover)

if st.session_state.status_msg:
    msg  = st.session_state.status_msg
    kind = st.session_state.status_type
    if kind == "success":
        st.success(msg)
    elif kind == "warning":
        st.warning(msg)
    else:
        st.info(msg)
    st.session_state.status_msg = ""

# ─────────────────────────────────────────────────────────────
# SIDEBAR — connection export / import
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Brain Settings")
    st.caption(
        "Graph resets each **calendar day**; the prior day is archived as "
        "`graph_archive/graph_YYYY-MM-DD.json`. While you work, each save also updates "
        "`brain_by_day/brain_YYYY-MM-DD.json` for that calendar date. **PNG** / **PDF** on the graph toolbar for images."
    )
    st.caption(f"connections.json: {len(st.session_state.nodes)} nodes, {len(st.session_state.edges)} edges")
    st.checkbox(
        "Auto-link new nodes to Active verse",
        key="auto_link_to_active",
        help="When enabled, newly added nodes are connected to the current Active verse.",
    )

    st.markdown("---")
    with st.expander("📅 Graph calendar (by day)", expanded=False):
        render_graph_calendar_sidebar()

    st.markdown("---")
    render_notes_sidebar()

    st.markdown("---")
    if st.button("🗑 Clear All Connections"):
        st.session_state.nodes  = []
        st.session_state.edges  = []
        st.session_state.active_verse = None
        _persist()
        st.rerun()

    st.markdown("---")
    if st.session_state.nodes:
        export = json.dumps({"nodes": st.session_state.nodes, "edges": st.session_state.edges}, indent=2)
        st.download_button(
            "⬇ Export connections.json",
            data=export,
            file_name="connections.json",
            mime="application/json",
        )

    uploaded = st.file_uploader("⬆ Import connections.json", type="json")
    if uploaded:
        try:
            data = json.load(uploaded)
            st.session_state.nodes = data.get("nodes", [])
            st.session_state.edges = data.get("edges", [])
            _persist()
            st.success("Imported successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Import failed: {e}")

    notes_export = json.dumps(
        {
            "verse_notes": load_verse_notes(),
            "edge_notes": load_edge_notes(),
            "memorization": st.session_state.get("verse_memorization", {}),
        },
        indent=2,
        ensure_ascii=False,
    )
    st.download_button(
        "⬇ Export notes (JSON)",
        data=notes_export,
        file_name="nexus_notes.json",
        mime="application/json",
        help="Includes verse_notes, edge_notes, and memorization flags.",
    )
    notes_up = st.file_uploader("⬆ Import notes (JSON)", type="json", key="notes_import_uploader")
    if notes_up:
        try:
            nd = json.load(notes_up)
            if isinstance(nd.get("verse_notes"), dict):
                save_verse_notes(nd["verse_notes"])
            if isinstance(nd.get("edge_notes"), dict):
                save_edge_notes(nd["edge_notes"])
            if isinstance(nd.get("memorization"), dict):
                mm: dict[str, bool] = {}
                for k, v in nd["memorization"].items():
                    if isinstance(v, bool):
                        mm[str(k)] = v
                    elif v in (1, "1", "true", "True"):
                        mm[str(k)] = True
                    elif v in (0, "0", "false", "False"):
                        mm[str(k)] = False
                st.session_state.verse_memorization = mm
                save_memorization_file(mm)
                sync_node_colors_in_session()
                _persist()
            st.success("Notes imported.")
            st.rerun()
        except Exception as e:
            st.error(f"Notes import failed: {e}")

    st.markdown("---")
    if _kjv_local_mtime() > 0:
        st.caption(
            f"Bible text: **local KJV** (`{os.path.basename(KJV_LOCAL_FILE)}`) — instant load; "
            "no network for verses."
        )
    else:
        st.caption(
            "Bible text: **KJV** via bible-api.com (then WEB if needed). "
            f"Use **Download local KJV** once for offline speed (~1–2 MB → `{os.path.basename(KJV_LOCAL_FILE)}`)."
        )
        if st.button("Download local KJV (one-time)", key="btn_dl_kjv_local", use_container_width=True):
            ok, msg = download_kjv_to_local_file()
            if ok:
                st.session_state.status_msg = msg
                st.session_state.status_type = "success"
            else:
                st.session_state.status_msg = f"Download failed: {msg}"
                st.session_state.status_type = "warning"
            st.rerun()
    st.caption("Graph: Cytoscape.js (embedded — scroll wheel zoom in graph frame)")
    st.caption("Schedule: GVCC 3-Column Plan")
