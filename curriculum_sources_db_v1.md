# Punjabi Conversational App: Core Database Schema & Content

This document serves as the foundational data source (the "database") that powers the app's conversational-first curriculum. Every entry includes the phonetic Romanization, the eventual Gurmukhi script (for later units), literal translations, and the "Vibe Check" (cultural context) to appeal to the Gen Z / Diaspora audience.

## Lesson Schema
```json
{
  "id": "phrase_001",
  "romanized": "Ki haal aa?",
  "gurmukhi": "ਕੀ ਹਾਲ ਆ?",
  "english_meaning": "How are you?",
  "literal_meaning": "What is the condition?",
  "dialect": "Majhi",
  "category": "Greeting",
  "vibe_check": "The most standard 'What's up?'. It's casual but polite enough for aunties."
}
```

---

## Unit 1: The Basics (Vibes & Greetings)
*Goal: Get learners speaking the most common daily phrases immediately.*

| Romanized (Phonetic) | Gurmukhi | Conversational Meaning | Literal Meaning | Vibe Check (Cultural Note) |
| :--- | :--- | :--- | :--- | :--- |
| **Sat Sri Akal** | ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ | Hello / Greetings | God is the ultimate truth | The universal greeting. Fold your hands when saying this to elders to max out your respect points. |
| **Ki haal aa?** | ਕੀ ਹਾਲ ਆ? | How are you? | What is the condition? | Standard "How are you?". Use with friends or family. |
| **Hor ki chalda?** | ਹੋਰ ਕੀ ਚੱਲਦਾ? | What's up? / What else is going on? | What else is walking? | Very casual. Best used when catching up with a cousin or friend. |
| **Vadhiya!** | ਵਧੀਆ! | Great! / Doing well! | Splendid / Increased | The standard response to "Ki haal aa?". Keep the energy high when saying it. |
| **Hanji / Nahi ji** | ਹਾਂਜੀ / ਨਹੀਂ ਜੀ | Yes / No (Polite) | Yes (with respect) / No (with respect) | Adding "ji" at the end of yes or no instantly makes you sound respectful. Use with parents and elders. |

## Unit 2: High-Frequency "Action" Verbs
*Goal: Teach the core verbs needed to construct 80% of daily sentences.*

| Romanized (Phonetic) | Gurmukhi | Conversational Meaning | Root Verb | Vibe Check (Cultural Note) |
| :--- | :--- | :--- | :--- | :--- |
| **Karna** | ਕਰਨਾ | To do | Kar (ਕਰ) | The ultimate helper verb. You attach "karna" to English words constantly (e.g., "Phone karna" = to make a phone call). |
| **Jaana** | ਜਾਣਾ | To go | Jaa (ਜਾ) | Used for movement. "Main jaana aa" (I have to go). |
| **Khana** | ਖਾਣਾ | To eat | Khaa (ਖਾ) | Essential for Punjabi hospitality. You will hear "Roti khali?" (Did you eat?) constantly. |
| **Hona** | ਹੋਣਾ | To be / happen | Ho (ਹੋ) | "Ki ho gaya?" (What happened?). Very common in dramatic situations. |

## Unit 3: The "Cool" Factor (Slang & Expressing Emotion)
*Goal: Teach vocabulary that makes the user sound native, modern, and playful.*

| Romanized (Phonetic) | Gurmukhi | Conversational Meaning | Literal Meaning | Vibe Check (Cultural Note) |
| :--- | :--- | :--- | :--- | :--- |
| **Ghaint** | ਘੈਂਟ | Cool / Awesome | N/A | High praise. Use it for a great outfit, a good song, or a fun plan. "Outfit badi ghaint aa!" |
| **Att** | ਅੱਤ | Ultimate / Fire / Crazy good | The end / Extreme | When something is beyond "ghaint". Often used in music. "Att kara diti!" (You killed it!). |
| **Siaapa** | ਸਿਆਪਾ | A huge mess / Headache / Drama | Mourning / Grief | When family drama hits or you lose your keys, it's a "siaapa". |
| **Thand rakh** | ਠੰਢ ਰੱਖ | Take a chill pill / Calm down | Keep cold | Use this when your friend is stressing out over nothing. |
| **Jugaad** | ਜੁਗਾੜ | A hack / clever workaround | N/A | The quintessential South Asian concept of making things work with limited resources. |

## Unit 4: Family & Relationships (Navigating the Pind)
*Goal: Demystify the complex family tree terminology, which is crucial for diaspora learners.*

| Term | Gurmukhi | Relation | Context |
| :--- | :--- | :--- | :--- |
| **Masi** | ਮਾਸੀ | Mother's sister | Your mom's side is usually the "fun" side. Masi is like a second mom. |
| **Bhuji / Bua** | ਭੂਆ | Father's sister | Often stereotyped in pop culture as the strict aunt who complains at weddings! |
| **Chacha** | ਚਾਚਾ | Father's younger brother | Your dad's younger brother. His wife is your "Chachi". |
| **Taaya** | ਤਾਇਆ | Father's older brother | Your dad's older brother. Holds a lot of respect in the family hierarchy. |
| **Mama** | ਮਾਮਾ | Mother's brother | The maternal uncle. Usually the one sneaking you money before you leave. |

---

## Pedagogical Note for App Developers:
- **Audio Prompts:** Every single phrase above MUST have high-quality Majhi audio attached to it in the app's backend database.
- **Progression:** The Gurmukhi text is present in the database, but the app UI should hide it behind a toggle or reserve it entirely for Unit 5, so the user focuses strictly on the Romanized pronunciation and audio first.
