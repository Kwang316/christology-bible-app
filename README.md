# ✝ Intro to the Bible

A beginner-friendly Bible Q&A application built with Streamlit.  
Ask any question — receive direct scripture quotes in canonical order alongside approved commentary.

---

## Mission

This app exists to make Scripture accessible to anyone asking sincere questions.  
It does **not** summarize or paraphrase the Bible. It quotes directly.  
When you ask *"What does the Bible say about math?"*, you get the actual verses — numbered, ordered Genesis to Revelation — plus optional commentary from trusted public-domain authors.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the Q&A app
streamlit run app.py

# 3. (Optional) Launch the full Zettelkasten graph app
streamlit run app_zettelkasten.py
```

On first launch, click **"Download KJV"** in the sidebar to cache the Bible locally (~1–2 MB).  
All subsequent searches are instant and offline.

---

## Q&A Engine — How It Works

1. You type a topic: `"What does the Bible say about math?"`
2. The engine expands your query into KJV keywords:  
   `math` → `["number", "count", "measure", "multiply", "numbered", "counted", "measured"]`
3. Every verse in the KJV is searched for those words (word-boundary match)
4. Results are sorted in **canonical Bible order** (Genesis → Revelation)
5. Matched keywords are highlighted in the verse text
6. Approved commentary excerpts are shown separately — clearly attributed

---

## File Structure

```
files/
├── app.py                    ← Q&A app (main entry point)
├── app_zettelkasten.py       ← Full Zettelkasten / graph app (preserved)
├── bible_search.py           ← KJV keyword search engine + topic map
├── commentary.py             ← Approved sources manager
├── schedule_data.py          ← GVCC reading schedule data
├── requirements.txt          ← Python dependencies
├── sources/
│   ├── manifest.json         ← Approved commentary registry
│   ├── matthew_henry_excerpts.txt
│   └── spurgeon_treasury_excerpts.txt
└── .gitignore
```

---

## Adding Approved Commentary

1. Place a `.txt` file in `sources/` (paragraphs separated by blank lines)
2. Open the app → **Approved Sources** page → fill in the registration form
3. Check **"Approve immediately"** to make it searchable at once

Or edit `sources/manifest.json` directly:

```json
{
  "sources": [
    {
      "author": "Your Author",
      "title": "Work Title",
      "year": 1885,
      "file": "your_file.txt",
      "description": "Brief description.",
      "approved": true
    }
  ]
}
```

Only sources with `"approved": true` appear in search results.

---

## Example Queries

| Question | Keywords searched |
|---|---|
| math | number, count, measure, multiply |
| love | love, charity, loveth, beloved |
| fear | fear, afraid, terror, dread |
| wisdom | wisdom, wise, understanding, knowledge |
| prayer | pray, prayer, supplication |

---

## Bible Text

- **Translation**: King James Version (KJV), 1611 — Public Domain
- **Source**: [thiagobodruk/bible](https://github.com/thiagobodruk/bible)
- **Storage**: Downloaded once to `kjv_by_chapter.json` (git-ignored)

---

## Pushing to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/christology-bible-app.git
git push -u origin main
```

---

*Scripture quoted from the King James Version (1611), public domain.*  
*Commentary from public-domain works (pre-1928).*
