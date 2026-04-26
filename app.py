"""
Intro to the Bible — Q&A Application
Ask any question and receive direct Bible verse quotes in canonical order.
"""

import os
import json
import requests
import streamlit as st

import bible_search as bs
import commentary as cm

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Intro to the Bible",
    page_icon="✝",
    layout="wide",
    initial_sidebar_state="expanded",
)

KJV_LOCAL_FILE = os.path.join(os.path.dirname(__file__), "kjv_by_chapter.json")
KJV_SOURCE_JSON_URL = (
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"
)

# ──────────────────────────────────────────────────────────────
# STYLES
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --cream:   #fdf8f0;
  --paper:   #fff9f2;
  --border:  #e8ddd0;
  --ink:     #1a1208;
  --ink-mid: #4a3f30;
  --ink-dim: #7a6f60;
  --gold:    #b5860e;
  --blue:    #1a4a8a;
  --green:   #1a5c30;
  --shadow:  rgba(26, 18, 8, 0.08);
}

html, body, .stApp {
  background-color: var(--cream) !important;
  font-family: 'Inter', system-ui, sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }

.app-header {
  text-align: center;
  padding: 2rem 1rem 1.5rem;
  border-bottom: 2px solid var(--border);
  margin-bottom: 2rem;
}
.app-header h1 {
  font-family: 'Merriweather', Georgia, serif;
  font-size: 2.2rem;
  color: var(--ink);
  margin: 0 0 0.4rem;
}
.app-header p { color: var(--ink-mid); font-size: 1rem; margin: 0; }

.search-label {
  font-family: 'Merriweather', Georgia, serif;
  font-size: 1.25rem;
  color: var(--ink);
  text-align: center;
  margin-bottom: 0.75rem;
}

.badge-ot {
  display: inline-block; background: #fef3c7; color: #92400e;
  font-size: 0.68rem; font-weight: 600; padding: 2px 8px;
  border-radius: 999px; letter-spacing: 0.05em;
  text-transform: uppercase; margin-right: 0.4rem;
}
.badge-nt {
  display: inline-block; background: #dbeafe; color: #1e3a8a;
  font-size: 0.68rem; font-weight: 600; padding: 2px 8px;
  border-radius: 999px; letter-spacing: 0.05em;
  text-transform: uppercase; margin-right: 0.4rem;
}

.verse-card {
  background: var(--paper); border: 1px solid var(--border);
  border-left: 4px solid var(--gold); border-radius: 8px;
  padding: 1rem 1.25rem; margin-bottom: 0.9rem;
  box-shadow: 0 1px 4px var(--shadow);
}
.verse-card.nt { border-left-color: var(--blue); }
.verse-ref {
  font-size: 0.78rem; font-weight: 700; color: var(--ink-dim);
  letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.35rem;
}
.verse-text {
  font-family: 'Merriweather', Georgia, serif;
  font-size: 1.05rem; line-height: 1.75; color: var(--ink);
}
.verse-text mark {
  background: #fef08a; color: var(--ink); border-radius: 2px; padding: 0 1px;
}

.commentary-card {
  background: #f0f7f0; border: 1px solid #c8dfc8;
  border-left: 4px solid var(--green); border-radius: 8px;
  padding: 1rem 1.25rem; margin-bottom: 0.9rem;
  box-shadow: 0 1px 4px var(--shadow);
}
.commentary-author {
  font-size: 0.78rem; font-weight: 700; color: #1a5c30; margin-bottom: 0.3rem;
}
.commentary-text {
  font-family: 'Merriweather', Georgia, serif;
  font-size: 0.95rem; line-height: 1.7;
  color: var(--ink-mid); font-style: italic;
}

.result-summary {
  font-size: 0.88rem; color: var(--ink-dim);
  margin-bottom: 1.25rem; padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# KJV HELPERS
# ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _load_kjv_cached(mtime: float) -> dict | None:
    return bs.load_kjv(KJV_LOCAL_FILE)

def _kjv_mtime() -> float:
    try:
        if os.path.isfile(KJV_LOCAL_FILE) and os.path.getsize(KJV_LOCAL_FILE) > 64:
            return os.path.getmtime(KJV_LOCAL_FILE)
    except OSError:
        pass
    return 0.0

def _download_kjv() -> tuple[bool, str]:
    try:
        r = requests.get(KJV_SOURCE_JSON_URL, timeout=180)
        r.raise_for_status()
        raw = r.json()
    except Exception as e:
        return False, str(e)

    BOOK_NAMES = [
        "Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth",
        "1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra",
        "Nehemiah","Esther","Job","Psalms","Proverbs","Ecclesiastes","Song of Solomon",
        "Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos",
        "Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah",
        "Malachi","Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians",
        "2 Corinthians","Galatians","Ephesians","Philippians","Colossians",
        "1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon",
        "Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation",
    ]
    out: dict = {}
    for bi, book_data in enumerate(raw):
        if bi >= len(BOOK_NAMES):
            break
        name = BOOK_NAMES[bi]
        out[name] = {}
        for ci, ch in enumerate(book_data.get("chapters", []), start=1):
            rows = [{"verse": vi, "text": t} for vi, t in enumerate(ch, start=1)]
            if rows:
                out[name][str(ci)] = rows
    try:
        with open(KJV_LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    except OSError as e:
        return False, str(e)
    _load_kjv_cached.clear()
    return True, f"Saved {len(out)} books to kjv_by_chapter.json."

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✝ Menu")
    page = st.radio(
        "Mode",
        ["Q&A — What does the Bible say?", "Browse by Book & Chapter", "Approved Sources"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Bible Text**")
    has_local = _kjv_mtime() > 0
    if has_local:
        st.success("Local KJV ready — instant search.", icon="✓")
    else:
        st.warning("Local KJV not found.")
        if st.button("Download KJV (one-time, ~1–2 MB)", use_container_width=True):
            with st.spinner("Downloading…"):
                ok, msg = _download_kjv()
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(f"Failed: {msg}")
    st.markdown("---")
    st.caption("KJV · Public Domain")
    st.caption("Graph view: `streamlit run app_zettelkasten.py`")

# ──────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <h1>✝ Intro to the Bible</h1>
  <p>Ask a question — receive direct scripture quotes in canonical order</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# PAGE: Q&A
# ──────────────────────────────────────────────────────────────
if page == "Q&A — What does the Bible say?":
    st.markdown('<div class="search-label">What does the Bible say about…?</div>', unsafe_allow_html=True)

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            "topic",
            placeholder="e.g. love, math, prayer, forgiveness, wisdom…",
            label_visibility="collapsed",
            key="main_query",
        )
    with col_btn:
        search_clicked = st.button("Search", type="primary", use_container_width=True)

    show_commentary = st.toggle("Include approved commentary excerpts", value=True)

    if query and (search_clicked or st.session_state.get("main_query")):
        mtime = _kjv_mtime()
        if mtime <= 0:
            st.warning("Please download the local KJV file first using the sidebar button.")
            st.stop()

        kjv = _load_kjv_cached(mtime)
        if not kjv:
            st.error("Could not load KJV file. Try re-downloading from the sidebar.")
            st.stop()

        keywords = bs.expand_query(query)
        results = bs.search_kjv(kjv, keywords, max_results=60)

        if not results:
            st.info(
                f"No verses found for **{query}**. "
                "Try a broader keyword (e.g. 'love', 'wisdom', 'fear')."
            )
        else:
            ot_count = sum(1 for r in results if r["testament"] == "OT")
            nt_count = len(results) - ot_count
            st.markdown(
                f'<div class="result-summary">'
                f'<strong>{len(results)}</strong> verses · '
                f'<strong>{ot_count}</strong> Old Testament · '
                f'<strong>{nt_count}</strong> New Testament · '
                f'Search terms: <em>{", ".join(keywords[:6])}</em>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if show_commentary:
                commentary_results = cm.search_commentary(keywords)
                if commentary_results:
                    with st.expander(f"📖 Commentary ({len(commentary_results)} excerpts)", expanded=True):
                        for c in commentary_results:
                            st.markdown(
                                f'<div class="commentary-card">'
                                f'<div class="commentary-author">'
                                f'{c["author"]} — <em>{c["title"]}</em> ({c["year"]})'
                                f'</div>'
                                f'<div class="commentary-text">{c["excerpt"]}</div>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

            st.markdown("### Scripture — King James Version")
            for r in results:
                badge = "badge-ot" if r["testament"] == "OT" else "badge-nt"
                card  = "verse-card" if r["testament"] == "OT" else "verse-card nt"
                highlighted = bs.highlight_keywords(r["text"], r["matched_keywords"])
                st.markdown(
                    f'<div class="{card}">'
                    f'<div class="verse-ref">'
                    f'<span class="{badge}">{r["testament"]}</span>{r["reference"]}'
                    f'</div>'
                    f'<div class="verse-text">"{highlighted}"</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

# ──────────────────────────────────────────────────────────────
# PAGE: BROWSE
# ──────────────────────────────────────────────────────────────
elif page == "Browse by Book & Chapter":
    mtime = _kjv_mtime()
    if mtime <= 0:
        st.warning("Please download the local KJV file first.")
        st.stop()
    kjv = _load_kjv_cached(mtime)
    if not kjv:
        st.error("Could not load KJV file.")
        st.stop()

    col_book, col_ch = st.columns([2, 1])
    with col_book:
        book = st.selectbox("Book", bs.CANONICAL_ORDER)
    with col_ch:
        chapter_data = kjv.get(book, {})
        chapter_nums = sorted(int(c) for c in chapter_data.keys())
        chapter = st.selectbox("Chapter", chapter_nums if chapter_nums else [1])

    verses = chapter_data.get(str(chapter), [])
    if not verses:
        st.info("No verses found.")
    else:
        st.markdown(f"### {book} {chapter} — KJV")
        for v in verses:
            st.markdown(
                f'<div class="verse-card">'
                f'<div class="verse-ref">{book} {chapter}:{v.get("verse","?")}</div>'
                f'<div class="verse-text">"{v.get("text","")}"</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ──────────────────────────────────────────────────────────────
# PAGE: SOURCES
# ──────────────────────────────────────────────────────────────
elif page == "Approved Sources":
    st.markdown("### Approved Commentary Sources")
    st.caption(
        "Approved authors are quoted alongside Bible verses in search results. "
        "Add a `.txt` file to `sources/` and register it below."
    )

    sources = cm.list_approved_sources()
    if not sources:
        st.info("No approved sources yet.")
    else:
        for s in sources:
            with st.expander(f"**{s['author']}** — {s['title']} ({s['year']})"):
                st.write(s.get("description", ""))
                fp = os.path.join(os.path.dirname(__file__), "sources", s["file"])
                st.caption(f"`sources/{s['file']}` · {'✓ Found' if os.path.isfile(fp) else '✗ File missing'}")

    st.markdown("---")
    st.markdown("#### Register a New Source")
    with st.form("add_source"):
        c1, c2 = st.columns(2)
        with c1:
            new_author = st.text_input("Author name")
            new_title  = st.text_input("Work title")
        with c2:
            new_year = st.text_input("Year", placeholder="e.g. 1706")
            new_file = st.text_input("Filename in sources/", placeholder="e.g. my_commentary.txt")
        new_desc     = st.text_area("Description (optional)")
        new_approved = st.checkbox("Approve immediately")
        if st.form_submit_button("Register Source"):
            if not all([new_author, new_title, new_file]):
                st.error("Author, title, and filename are required.")
            else:
                ok = cm.add_source_to_manifest(
                    author=new_author, title=new_title, year=new_year,
                    file_name=new_file, description=new_desc, approved=new_approved,
                )
                st.success("Registered." if ok else "A source with that filename already exists.")
