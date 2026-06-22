# Punjabi Conversational Learning App - Curriculum & Data Sources Plan

As a linguist and Punjabi educator, building an app that prioritizes **conversational fluency and cultural nuance** over immediate script acquisition (Gurmukhi/Shahmukhi) requires a unique pedagogical approach. The traditional method of teaching alphabets first often bogs learners down. By focusing on phonetics, listening comprehension, and high-frequency colloquialisms first, we can get learners speaking on day one.

Here is the proposed blueprint and the required sources to build the content for this app.

## 1. Pedagogical Strategy: The "Audio-First" Approach

Before introducing the script, the app will rely on:
*   **Romanized Transliteration:** Using a consistent phonetic English spelling to help learners pronounce words correctly.
*   **Tonal Awareness:** Punjabi is a tonal language (rare among Indo-Aryan languages). We must emphasize the high-falling, low-rising, and neutral tones early on (e.g., *kòṛā* 'horse' vs *koṛā* 'whip' vs *kóṛā* 'leper').
*   **Dialect Focus:** We will strictly adhere to the **Majhi** dialect (the standard dialect of Amritsar/Lahore) for consistency and foundation.

## 2. Target Audience & App Tone

The primary audience includes diaspora/heritage speakers who have some passive understanding but lack speaking confidence, as well as Gen Z learners (especially women/girls) who are drawn to the language's aesthetic and culture but have no prior background.
*   **Vibe:** The app must feel modern, playful, and highly aesthetic—moving away from the dry, textbook feel of traditional language apps.
*   **Cultural Context:** We will provide bite-sized, engaging cultural notes that explain *why* we say things a certain way, making the language feel accessible and vibrant.

## 2. Core Curriculum & Data Sources

To build the app's content, we will need to aggregate data from the following types of sources:

### A. High-Frequency Spoken Corpora (The Foundation)
Instead of formal dictionary words, we need to teach the 1,000 most commonly spoken words.
*   **Sources:**
    *   **EMILLE/CIIL Punjabi Corpus:** A large corpus of spoken and written Punjabi. We will extract only the spoken transcriptions to build a frequency list of verbs and nouns.
    *   **Linguistic Data Consortium for Indian Languages (LDC-IL):** For phonetic data and spoken language datasets.
    *   **Subtitle Databases:** Scraping Punjabi movie subtitles (from platforms like OpenSubtitles) and running frequency analysis to find the most commonly used daily conversational phrases (e.g., "Ki haal aa?", "Kidda?", "Theek aa").

### B. Colloquialisms & Slang (The "Cool" Factor)
To make learners sound natural and understand pop culture.
*   **Sources:**
    *   **Punjabi Pop Music Lyrics:** Analyzing lyrics from artists like Diljit Dosanjh, Karan Aujla, and AP Dhillon. Music is the biggest export of Punjabi culture.
    *   **Slang Glossaries:** Terms like *Ghaint* (cool/awesome), *Att* (extreme/ultimate), *Siaapa* (mess/trouble), *Vella* (idle), *Jugaad* (hack/workaround).
    *   **Social Media:** Analyzing common phrases used by Punjabi influencers and YouTubers.

### C. Idioms (Muhavare) and Proverbs (Akhaan) (Cultural Nuance)
Punjabi is a highly metaphorical language. Understanding idioms is key to conversational fluency.
*   **Sources:**
    *   **Traditional Academic Texts:** Books like *Punjabi Muhavare te Akhaan* compiled by language boards (e.g., Punjab School Education Board).
    *   **Examples to include:**
        *   *Siaapa* (Literal: mourning; Conversational: A huge mess/problem).
        *   *Thand rakh* (Literal: Keep cold; Conversational: Take a chill pill).
        *   *Kutte bhaunkde rehnde ne, haathi langh jaande ne* (Dogs bark, but elephants pass by - ignore the haters).

### D. Audio & Pronunciation Resources
Since this is an audio-first app, high-quality native audio is paramount.
*   **Sources:**
    *   **Native Voice Actors:** We will source native speakers of the Majhi dialect to ensure consistent pronunciation and tone.
    *   **Forvo / Wikimedia Commons:** For open-source pronunciation audio of base vocabulary.
    *   **Podcasts / YouTube:** Content from channels like "Basics of Sikhi" (conversational aspects) or creators like "Satdeep Singh" (short films for listening comprehension).

## 3. App Progression Flow (Phase 1)

1.  **Unit 1: The Basics of Survival:** Greetings, politeness, asking questions. Focus on tones and rhythm. (e.g., "Sat Sri Akal", "Hor ki chalda?", "Hanji/Nahi").
2.  **Unit 2: The Action Words:** High-frequency verbs (Karna - to do, Hona - to be, Jaana - to go, Aana - to come, Khana - to eat, Peena - to drink).
3.  **Unit 3: Expressing Emotion & Slang:** How to express excitement (Ghaint!), frustration (Siaapa!), or relaxation (Thand rakh).
4.  **Unit 4: Navigating Relationships:** Family terms (which are highly specific in Punjabi, e.g., Chacha vs Taaya for uncle).
5.  **Unit 5: Introduction to Script:** Only after conversational confidence is built do we introduce the **Gurmukhi** script.

## Phase 1: Content Repository Architecture & Curation Plan

Based on your initial source list, here is the structured strategy to build a deep, high-quality content repository suitable for a Duolingo-style app.

### 1. Data Ingestion & Extraction Strategy
We will break down the ingestion into three distinct pipelines based on the source format:

*   **Pipeline A: Structured Text & Vocab (Dictionaries, Phrasebooks)**
    *   **Action:** Scrape HTML/JSON from sites like *eLearnPunjabi*, *PunjabiGuide*, and *Omniglot*.
    *   **Tools:** Python (`BeautifulSoup`, `requests`).
    *   **Output:** Base JSON vocabulary lists with English, Romanized Punjabi, and Gurmukhi.
*   **Pipeline B: Unstructured Text (PDFs, Books, Proverbs)**
    *   **Action:** Download public domain PDFs (e.g., *Akhaanan Di Khaan*, *Heer Waris Shah*) from Panjab Digital Library and Archive.org. Use OCR for Gurmukhi/Shahmukhi and LLMs to parse text into structured JSON.
    *   **Tools:** Python (`PyMuPDF`, `Tesseract OCR`), LLM processing for structured extraction.
    *   **Output:** Rich literary and cultural JSON items (Idioms, Example Sentences).
*   **Pipeline C: Audio & Conversational Mining (YouTube, Media)**
    *   **Action:** Extract audio and auto-generated transcripts from YouTube channels (*Punjabi With Navrup*, *Colloquial Punjabi*).
    *   **Tools:** `yt-dlp` for audio/transcripts, `whisper` for alignment if needed.
    *   **Output:** High-frequency conversational phrases with native Majhi audio snippets.

### 2. Proposed Tech Stack for Repository Building
To process and manage this repository before the app is built:
*   **Scripting Language:** Python (ideal for web scraping, PDF processing, and data manipulation).
*   **Data Validation:** `Pydantic` (Python) to strictly enforce your proposed JSON Schema for every vocabulary/dialogue item.
*   **Storage:** A local file-based repository following your proposed folder structure, acting as a NoSQL document database. We can eventually wrap this in a database if querying becomes complex.

### 3. Repository Folder Structure
We will adopt and expand upon your suggested structure:
```text
/punjabi-app-content
├── schemas/                  # Pydantic/JSON schemas for validation
├── raw_data/                 # Downloaded PDFs, raw HTML, full YouTube transcripts
├── processed_data/           # Validated JSON files
│   ├── vocab/                # Single words (e.g., family, food)
│   ├── dialogues/            # Conversational pairs
│   ├── proverbs/             # Idioms and cultural notes
│   └── literary/             # Excerpts from Heer Ranjha, etc.
├── media/                    
│   ├── audio/                # Cropped native audio files (.mp3)
│   └── images/               # Any cultural reference images
├── scripts/                  # Python ingestion pipelines and validation scripts
└── content_plan.md           # Tracking ingestion progress
```

### 4. Audio & Tonal Pipeline
Since Punjabi is tonal, audio isn't just an add-on; it's core to the data schema.
*   **Initial Phase:** Extract and crop clean audio from public domain sources and YouTube (giving credit/checking licenses).
*   **Tonal Tagging:** When processing vocabulary, use an LLM or manual review to explicitly tag the tone (`high`, `mid`, `low`) in the JSON.
*   **Future Phase:** Batch-generate scripts from our `processed_data` to give to native Majhi voice actors for consistent, studio-quality recording.

### 5. Execution Steps to Build the Repository
1.  **Initialize the Repository:** Create the folder structure and write the formal JSON Schema definitions.
2.  **Scrape the "Low-Hanging Fruit":** Build the base vocabulary by scraping *Omniglot* and *50Languages*. Validate into `vocab/`.
3.  **Process the PDFs:** Download the proverb PDFs, extract text, and structure them into `proverbs/`.
4.  **Audio Extraction:** Run `yt-dlp` on the selected conversational YouTube channels to build the `dialogues/` repository.

## User Review Required
> [!IMPORTANT]
> **Data Structure:** Does the expanded folder structure (separating `raw_data` from `processed_data`) work for your workflow?

> [!IMPORTANT]
> **Storage:** Are you comfortable keeping this as a JSON file-based repository initially, or would you prefer setting it up in a database (like SQLite or Postgres) from day one?

> [!IMPORTANT]
> **Starting Point:** Shall we begin by initializing the repository structure and writing the Python validation scripts for the schema you provided?
