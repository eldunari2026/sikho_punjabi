# Content Ingestion & Enrichment Plan

The app's goal is to get learners **speaking and interacting** with the language before introducing the Gurmukhi script. That means content quality is defined by conversational naturalness, cultural resonance, and tonal accuracy — not academic completeness.

---

## Status Summary

| Pipeline | Status | Items |
|---|---|---|
| A — Structured Vocab & Phrases | In Progress | 43 Omniglot phrases (roman field empty) |
| B — Proverbs & Literary | Not Started | 2 EPUBs downloaded |
| C — Multimedia & Dialogues | Not Started | — |
| D — Enrichment (LLM post-processing) | Not Started | — |

---

## Pipeline A: Structured Vocab & Phrases

Sources with clean structure (tables, HTML, JSON) that map directly to our `VocabularyItem` schema.

### A1. Omniglot Basic Phrases
- **Source:** `raw_data/omniglot_phrases.md` (already scraped)
- **Script:** `scripts/parse_omniglot.py`
- **Status:** `[x]` 43 JSON files in `processed_data/vocab/`
- **Gap:** `roman` field is empty for all 43 items — needs LLM romanization pass (see Pipeline D)

### A2. Punjabi University, Patiala — learnpunjabi.org
- **Source:** http://www.learnpunjabi.org/statistics.html
- **Content:** 500 most-common Punjabi words with audio. Also: 3,000+ words with pictures across 80 topics (http://www.learnpunjabi.org/vocabulary/vocabulary1.asp?id=23)
- **Format:** HTML (scrapable), audio files linked inline
- **Value:** Highest-priority vocab source — frequency-ranked and audio-paired. The 500-word list maps well to our Unit 1 and Unit 2 curriculum.
- **Status:** `[ ]` Not started

### A3. 50Languages — Vocab & Phrases
- **Source:** https://www.50languages.com/vocab/em/pa/ (vocab) + https://www.50languages.com/phrasebook/em/pa/ (phrases, 100 topics)
- **Format:** HTML, audio files available per item
- **Value:** Phrases cover 100 conversational topics with audio. Well-structured for scraping.
- **Status:** `[ ]` Not started

### A4. DiscoverSikhism — Vocab & Phrases
- **Source:**
  - Vocab pt. 1 (numbers, days, fruits, food, family, body, travel): http://www.discoversikhism.com/punjabi/punjabi_gurmukhi_vocabulary.html
  - Vocab pt. 2 (prepositions, questions, adverbs, pronouns, verbs): http://www.discoversikhism.com/punjabi/punjabi_gurmukhi_grammar.html
  - Phrases with audio: http://www.discoversikhism.com/punjabi/punjabi_gurmukhi_phrases.html
- **Format:** HTML tables, embedded audio
- **Value:** Good coverage of functional grammar vocab (pronouns, verbs, question words) which learnpunjabi.org may not cover as well.
- **Status:** `[ ]` Not started

### A5. eLearnPunjabi — Dialogues & Courses
- **Source:** https://www.elearnpunjabi.com/
- **Content:** Video dialogues, multimedia courses, greetings, daily conversations
- **Format:** HTML/video — will require manual review to identify scrapable assets vs. gated content
- **Value:** Dialogues are directly usable for `processed_data/dialogues/`. High curriculum alignment.
- **Status:** `[ ]` Needs site audit before scripting

### A6. Punjabi Akhaan (punjabi.com)
- **Source:** https://punjabi.com/akhaan
- **Content:** Online proverbs database
- **Format:** HTML (scrapable) — easier entry point than the PDF version
- **Value:** Quick win for `processed_data/proverbs/` before tackling the full EPUB
- **Status:** `[ ]` Not started

### A7. Sikhville PDFs — Thematic Vocab
- **Source:** http://www.sikhville.org/pdf/ (Colors, Fruits, Vegetables, Body Parts, Animals, Time, Nature)
- **Format:** PDFs — require extraction
- **Value:** Good thematic coverage for Unit 4+ (family, food, environment). Lower priority than learnpunjabi.org.
- **Status:** `[ ]` Not started

### A8. AQA GCSE Vocabulary List
- **Source:** https://amardeep0.github.io/learnPunjabi/files/Panjabi_VocabularyList_From_AQA_GCSE.pdf
- **Content:** Comprehensive topic-structured list (greetings, time, travel, culture, social issues, identity)
- **Format:** PDF — require extraction
- **Value:** Covers advanced/contextual vocab not in basic frequency lists. Good for Units 3–5.
- **Status:** `[ ]` Not started

---

## Pipeline B: Proverbs & Literary

Sources for idioms, proverbs, and cultural language depth. These feed `processed_data/proverbs/` and `processed_data/literary/`.

### B1. Saaday Akhaan — Dr. Shahbaz Malik (EPUB)
- **Source:** `raw_data/Saaday Akhaan - Dr. Shahbaz Malik - Book - ساڈے اکھان ـ ڈاکٹر شہباز ملک - کتاب.epub`
- **Content:** Shahmukhi Punjabi proverbs collection. Will require extraction + Gurmukhi transliteration.
- **Format:** EPUB (unzip → HTML/XML → parse). Script needed.
- **Value:** Deep, authentic proverb source. Shahmukhi text will need LLM conversion to Gurmukhi + romanization.
- **Status:** `[ ]` Not started — EPUB is downloaded

### B2. Heer Waris Shah (EPUB)
- **Source:** `raw_data/The Love Of Hir And Ranjha Waris Shah.epub`
- **Content:** Classic literary text — rich in metaphor, idiom, and cultural vocabulary
- **Format:** EPUB — same extraction approach as B1
- **Value:** Feeds `processed_data/literary/`. Primary use is extracting key phrases, not full text ingestion. Good for cultural depth notes.
- **Status:** `[ ]` Not started — EPUB is downloaded

### B3. Akhaanan Di Khaan — Panjab Digital Library
- **Source:** http://www.panjabdigilib.org/webuser/searches/displayPage.jsp?ID=14568&page=1&CategoryID=1&Searched=
- **Content:** Scanned proverbs book. Likely image-based PDF requiring OCR.
- **Format:** Scanned pages — needs Tesseract OCR + LLM structuring
- **Value:** Most comprehensive proverb source but highest extraction effort. Lower priority given B1 is already downloaded.
- **Status:** `[ ]` Not started — defer until B1 is complete

---

## Pipeline C: Multimedia & Dialogues

Sources that yield conversational phrases with native audio. These feed `processed_data/dialogues/` and `media/audio/`.

### C1. Punjabi With Navrup (YouTube)
- **Tool:** `yt-dlp`
- **Content:** Conversational Punjabi lessons — Majhi dialect, beginner-friendly
- **Value:** Native audio snippets for dialogue entries
- **Status:** `[ ]` Not started

### C2. Colloquial Punjabi — AmrinderMK (YouTube)
- **Tool:** `yt-dlp`
- **Value:** Natural speech patterns, informal register — aligns with Gen Z/diaspora tone
- **Status:** `[ ]` Not started

### C3. Punjabi Pop Music Lyrics
- **Sources:** Karan Aujla, AP Dhillon, Diljit Dosanjh lyrics — available via Genius API or scraping
- **Content:** Slang, colloquialisms, modern register
- **Value:** Direct pipeline to Unit 3 (Cool Factor) content. High appeal to target audience.
- **Method:** Frequency analysis on lyric corpora to surface the most-used slang terms → enrich with cultural notes
- **Status:** `[ ]` Not started — needs source decision (Genius API vs. manual curation)

### C4. Sikh Missionary Society — Intermediate Course
- **Source:** https://www.sikhmissionarysociety.org/sms/smspublications/AnIntermediateLevelJointCourseInPanjabi.pdf (pages 5–55)
- **Content:** Structured vocab by topic: body, food, clothes, family, school, seasons, numbers, pronouns, verbs
- **Format:** PDF
- **Value:** Well-organized intermediate bridge content for Units 3–5
- **Status:** `[ ]` Not started

---

## Pipeline D: Enrichment (LLM Post-Processing)

This pipeline runs *after* initial ingestion to fill structural gaps that source data can't provide. No new sources — operates on `processed_data/`.

### D1. Romanization
- **Problem:** Omniglot (and likely Sikhville, DiscoverSikhism) don't provide romanization. All 43 current items have `roman: ""`.
- **Method:** LLM batch pass — input Gurmukhi, output Majhi-dialect romanization following our phonetic conventions (tonal markers: `ò`, `ó`, etc.)
- **Priority:** High — `roman` field is core to the app experience

### D2. Tonal Tagging
- **Problem:** No source provides syllable-level tone data (`high`, `mid`, `low`).
- **Method:** LLM batch pass — input Gurmukhi + romanized, output tones array per syllable. Flag ambiguous cases for human review.
- **Priority:** Medium — needed before audio scripts are finalized

### D3. Cultural Notes (Vibe Check)
- **Problem:** Structured vocab sources have no cultural context. The `cultural_note` field is empty across all 43 ingested items.
- **Method:** LLM batch pass — input English + Gurmukhi + tags, generate a Gen Z/diaspora-toned cultural note in the voice of the curriculum (see `curriculum_sources_db_v1.md` for tone examples).
- **Priority:** Medium — high impact on app engagement

### D4. Deduplication
- **Problem:** Multiple sources will produce overlapping entries (e.g., "How are you?" appears in Omniglot, DiscoverSikhism, and 50Languages).
- **Method:** Post-ingestion script — fuzzy match on `english` + `gurmukhi`, merge best fields from duplicates (prefer audio URLs, prefer sources with tonal data).
- **Priority:** Run after all Pipeline A sources are ingested

---

## Ingestion Priority Order

Given curriculum sequencing (speak first, script later) and effort/value ratio:

1. **D1 — Romanize existing Omniglot items** (quick LLM pass, unblocks current data)
2. **A2 — learnpunjabi.org** (500 most common words + audio — foundational)
3. **A3 — 50Languages phrases** (100 conversational topics + audio)
4. **A6 — punjabi.com/akhaan** (quick web scrape for proverbs)
5. **B1 — Saaday Akhaan EPUB** (already downloaded, highest proverb value)
6. **A4 — DiscoverSikhism** (functional grammar vocab gap-fill)
7. **D3 — Cultural notes pass** (enrich all items with vibe_check)
8. **C3 — Punjabi pop lyrics** (Unit 3 slang content)
9. **C1/C2 — YouTube dialogues** (audio pipeline setup)
10. **D2 — Tonal tagging** (after core vocab is stable)
11. **B2 — Heer Waris Shah EPUB** (literary depth)
12. **B3 — Akhaanan Di Khaan** (OCR effort — last)
