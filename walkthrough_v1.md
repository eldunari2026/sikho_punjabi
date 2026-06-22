# Walkthrough: Punjabi App Curriculum & Sources

We have successfully built the core pedagogical foundation and sample database sources for the Punjabi conversational app.

## What Was Accomplished
Based on your parameters (Majhi dialect, Gurmukhi script later, Gen Z/Diaspora audience), I created a sample database of curriculum content.

1.  **Pedagogical Schema:** Created a JSON-style schema that dictates how the app will store data. Every entry requires:
    *   `romanized` (for early, phonetic reading)
    *   `gurmukhi` (for later script introduction)
    *   `english_meaning`
    *   `literal_meaning` (provides deep linguistic context)
    *   `vibe_check` (Gen Z-friendly cultural notes that make learning engaging)
2.  **Unit Generation:** Mapped out the first four core units to demonstrate the progression flow:
    *   *Unit 1:* The Basics (Vibes & Greetings)
    *   *Unit 2:* High-Frequency Action Verbs
    *   *Unit 3:* Slang & Expressing Emotion (The "Cool" Factor)
    *   *Unit 4:* Family & Relationships
3.  **Vocabulary Selection:** Curated specific words that are highly relevant to the diaspora and modern learners (e.g., *Ghaint*, *Siaapa*, *Att*).

## View the Work
You can view the exact data structure and the sample content in the compiled artifact here:
*   [Curriculum Sources Database](file:///Users/arjunsingh/.gemini/antigravity/brain/9a92ccee-fc37-4eab-ad0d-a8a8fbe5a0c5/curriculum_sources_db.md)

## Phase 1: Repository Architecture & Data Ingestion
Based on your instructions, we have successfully begun executing Phase 1 of the Content Repository architecture:

1. **Repository Structure Setup:** Created the `punjabi-app-content/` directory with a structured separation between `raw_data`, `processed_data/vocab`, `processed_data/dialogues`, and `media`.
2. **Schema Definition:** Wrote `schemas/schema.py` using `Pydantic` to enforce strict formatting for all JSON data items (requiring specific ID structures, tone lists, and part of speech identifiers).
3. **Pipeline A Execution (Vocab Scraper):** Wrote a native Python scraper (`scripts/parse_omniglot.py`) that successfully extracted and structured conversational phrase pairs from the Omniglot phrases list directly into 43 discrete JSON files in our repository.

## View the Work
* [Task Tracker](file:///Users/arjunsingh/Documents/Sikho_Punjabi/task_v1.md)
* [Content Tracking Plan](file:///Users/arjunsingh/Documents/Sikho_Punjabi/punjabi-app-content/content_plan.md)
* [JSON Schema Definition](file:///Users/arjunsingh/Documents/Sikho_Punjabi/punjabi-app-content/schemas/schema.py)
* [Omniglot Scraper Script](file:///Users/arjunsingh/Documents/Sikho_Punjabi/punjabi-app-content/scripts/parse_omniglot.py)

## Next Steps / Technical Note
* **Xcode Command Line Tools:** To execute `Pydantic` schema validations and install advanced packages (like `beautifulsoup4` or `yt-dlp`), the Mac requires the Xcode Command Line tools to be installed. We bypassed this using pure Python for the first script, but this will need to be resolved to run the full validation pipeline.
* **Pipeline B:** Moving on to unstructured text extraction from PDFs (like the Proverbs list).
