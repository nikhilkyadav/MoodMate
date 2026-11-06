# 🎵 MoodMate – Free AI Companion Chatbot with Mood-Based Music

**MoodMate** is an empathetic, conversational AI companion that chats with you, detects your emotional state, recommends songs that match and gently uplift your mood using the **iso-principle**, streams the chosen music in the background without interrupting the conversation, and captures session feedback.

---

## 0. Ground Rules & 100% Free Guarantee

- **Zero Paid Dependencies**: No paid APIs, no subscription tiers, no credit card required.
- **Runs Locally on Normal Laptops**: Powered by local open-source models via [Ollama](https://ollama.com/) (e.g., Llama 3.2 3B or 1B), with optional free internet-based AI providers (Google Gemini Free Tier, Groq Free Tier, OpenRouter Free Models).
- **Free Official Music Playback**: Powered by the official **YouTube IFrame Player API** (free embed, no API key required).
- **Privacy & Security**: PII (name, email, phone number) is encrypted on disk using 256-bit AES (Fernet). Emails are HMAC-SHA256 hashed with a secret pepper. Passwords are salted and hashed with bcrypt.

---

## 1. System Architecture

```
                                  ┌──────────────────────────────┐
                                  │   Frontend (Vanilla JS/CSS)  │
                                  │  - Dynamic Mood Aura Themes  │
                                  │  - Persistent Mini Player    │
                                  │  - YouTube IFrame Player API │
                                  └──────────────┬───────────────┘
                                                 │ HTTP / REST
                                                 ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                FastAPI Backend Engine                                  │
│                                                                                        │
│  ┌────────────────────┐   ┌────────────────────────┐   ┌────────────────────────────┐  │
│  │   Auth & Crypto    │   │      Safety Guard      │   │        Music Engine        │  │
│  │  - Fernet AES-256  │   │ - Server-Side Keywords │   │ - music_cache.json         │  │
│  │  - HMAC-SHA256     │   │ - Multi-lingual        │   │ - fallback_songs.json      │  │
│  │  - bcrypt / PyJWT  │   │   (EN, HI, BN, Hinglish│   │ - yt-dlp metadata search   │  │
│  │  - slowapi Limiter │   │ - 24/7 Crisis Resource │   │ - YouTube oEmbed verify    │  │
│  └─────────┬──────────┘   └───────────┬────────────┘   └─────────────┬──────────────┘  │
│            │                          │                              │                 │
│            ▼                          ▼                              ▼                 │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                      Unified OpenAI-Compatible LLM Provider                      │  │
│  │        Ollama (Local) | Google Gemini | Groq | OpenRouter Free Models            │  │
│  │            - Compact JSON Prompts & Shared `parse_and_repair()`                  │  │
│  │            - Automatic retry & failover to default model                         │  │
│  └────────────────────────────────────┬─────────────────────────────────────────────┘  │
│                                       │                                                │
│                                       ▼                                                │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                 StorageInterface (Thread-safe FileLock openpyxl)                 │  │
│  │         moodmate_data.xlsx: Users | Sessions | Chats | Music_Log | Feedback      │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Free-Only Dependency Audit

Every library, tool, and service utilized by MoodMate is verified 100% free and open-source:

| Component / Library | Version | License | Cost | Purpose |
|---|---|---|---|---|
| **Python** | 3.11+ | PSF License | **$0.00** | Core programming language |
| **FastAPI** | >=0.110.0 | MIT License | **$0.00** | High-performance asynchronous web API framework |
| **Uvicorn** | >=0.29.0 | BSD-3-Clause | **$0.00** | Lightweight ASGI web server |
| **openpyxl** | >=3.1.2 | MIT License | **$0.00** | Concurrent spreadsheet data storage engine |
| **filelock** | >=3.13.1 | Unlicense / Public Domain | **$0.00** | Thread-safe and process-safe filesystem locks |
| **cryptography** | >=42.0.5 | Apache-2.0 / BSD | **$0.00** | Fernet symmetric 256-bit AES encryption for PII |
| **bcrypt** | >=4.1.2 | Apache-2.0 | **$0.00** | Password hashing with random salt rounds |
| **PyJWT** | >=2.8.0 | MIT License | **$0.00** | Stateless JWT authentication tokens |
| **slowapi** | >=0.1.9 | MIT License | **$0.00** | IP-based API rate limiting |
| **httpx** | >=0.27.0 | BSD-3-Clause | **$0.00** | Async HTTP client for OpenAI-compatible APIs |
| **yt-dlp** | >=2024.3.10 | Unlicense | **$0.00** | Metadata-only song search (`ytsearch1:`) without downloads |
| **python-dotenv** | >=1.0.1 | BSD-3-Clause | **$0.00** | Environment variable management |
| **Ollama** | Latest | MIT License | **$0.00** | Local, private inference engine (runs on your CPU/GPU) |
| **YouTube IFrame API** | v3 Embed | Free Official Embed | **$0.00** | Music playback without API keys or subscriptions |
| **Gemini Free Tier** | v1beta/openai | Free Developer Tier | **$0.00** | Optional Google AI Studio free tier (rate-limited) |
| **Groq Free Tier** | OpenAI-compat | Free Developer Tier | **$0.00** | Optional Groq Console free tier (rate-limited) |
| **OpenRouter Free** | OpenAI-compat | Free Model Endpoints | **$0.00** | Optional open-weights models ending with `:free` |

---

## 3. Project Structure

```
MoodMate/
├── backend/
│   ├── main.py               # FastAPI application, REST endpoints, and static mounts
│   ├── auth.py               # Registration, E.164 phone validation, bcrypt, and PyJWT
│   ├── crypto.py             # Fernet symmetric encryption and HMAC-SHA256 email hashing
│   ├── storage.py            # StorageInterface + ExcelStorage with filelock and retry queue
│   ├── llm.py                # Unified OpenAI-compatible provider, parse_and_repair, fallbacks
│   ├── safety.py             # Server-side crisis detector (EN, HI, BN, Hinglish) & helplines
│   ├── music.py              # Music engine: cache -> fallback -> yt-dlp -> replace
│   ├── mood.py               # Mood taxonomy, iso-principle definitions, system prompt builder
│   ├── admin_view.py         # Admin CLI tool: decrypt user PII with master Fernet key
│   └── test_moodmate.py      # Comprehensive 6-part test suite
├── frontend/
│   ├── index.html            # Semantic, accessible HTML5 interface
│   ├── style.css             # Dynamic mood theme gradients, dark/light mode, mobile-first
│   └── app.js                # Vanilla JS client, YouTube Player API, persistent playback
├── models.json               # Config-driven model directory (Ollama, Gemini, Groq, OpenRouter)
├── fallback_songs.json       # Curated verified songs (120 tracks across 10 moods in EN, HI, BN)
├── crisis_keywords.json      # Crisis & self-harm keyword database across 4 languages
├── crisis_resources.json     # 24/7 verified crisis helplines and regional placeholders
├── generate_keys.py          # Secure key generator for FERNET_KEY, EMAIL_PEPPER, JWT_SECRET
├── .env.example              # Template for environment settings
├── requirements.txt          # Python dependencies
└── README.md                 # Complete documentation and audit
```

---

## 4. Step-by-Step Setup Guide

### Step 1: Clone or Navigate to the Directory
```bash
cd MoodMate
```

### Step 2: Set Up Python Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Free Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Cryptographic Secrets
Run the key generator script to automatically populate your `.env` file with fresh keys:
```bash
python generate_keys.py
```
This generates:
- `FERNET_KEY`: A 256-bit URL-safe base64 encryption key.
- `EMAIL_PEPPER`: A 64-character random hex pepper for HMAC-SHA256 email indexing.
- `JWT_SECRET`: A secure token for signing user session tokens.

### Step 5: (Default Free Mode) Set Up Ollama for Local AI
MoodMate works 100% offline and free with [Ollama](https://ollama.com/):
1. Download and install Ollama from [ollama.com](https://ollama.com/).
2. Open your terminal and pull a lightweight model:
   ```bash
   # Recommended for standard laptops (fast and lightweight):
   ollama run llama3.2:3b
   
   # Or for low-RAM laptops (ultra-lightweight):
   ollama run llama3.2:1b

   # For strong multilingual Hindi/Bengali fluency:
   ollama run qwen2.5:3b
   ```
3. Ollama runs locally on `http://localhost:11434/v1`. No API keys or configurations are needed.

### Step 6: (Optional) Add Free Internet Cloud Keys
If you want to use cloud-based models in addition to Ollama, you can obtain completely free API keys:
- **Google Gemini**: Get a free key at [Google AI Studio](https://aistudio.google.com/) and paste it into `.env` as `GEMINI_API_KEY=...`
- **Groq**: Get a free key at [Groq Console](https://console.groq.com/) and paste it into `.env` as `GROQ_API_KEY=...`
- **OpenRouter**: Get a free key at [OpenRouter](https://openrouter.ai/) and paste it into `.env` as `OPENROUTER_API_KEY=...`

*Note: Free-tier limits and model names change over time. Verify current limits on the respective provider portals.*

### Step 7: Start MoodMate
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser and navigate to:
```
http://localhost:8000
```

---

## 5. Sample Excel Sheets (`moodmate_data.xlsx`)

After running a session, open `moodmate_data.xlsx` to view how data is isolated and secured:

### Sheet 1: `Users` (Encrypted PII vs Plaintext Metadata)
| user_id | email_hash | name_enc | email_enc | phone_enc | password_hash | preferred_model | created_at | last_login |
|---|---|---|---|---|---|---|---|---|
| `08b1612a-...` | `2de30c2aa84d...` | `gAAAAABq6jVG...` *(AES-256)* | `gAAAAABq6jVG...` *(AES-256)* | `gAAAAABq6jVG...` *(AES-256)* | `$2b$12$LiWf...` *(bcrypt)* | `gemini/gemini-2.0-flash` | `2026-11-04T00:25:58Z` | `2026-11-04T00:25:58Z` |

> Notice that name, email, and phone numbers are encrypted into random ciphertexts. The administrator cannot read PII without the master Fernet key.

### Sheet 2: `Sessions`
| session_id | user_id | start_time | end_time | initial_mood | final_mood | songs_played_count | models_used |
|---|---|---|---|---|---|---|---|
| `ecf4c0d3-...` | `08b1612a-...` | `2026-11-04T00:25:58Z` | `2026-11-04T00:26:00Z` | `sad` | `calm` | 1 | `ollama/llama3.2, gemini/gemini-2.0-flash` |

### Sheet 3: `Chats` (Plaintext Readable for Review)
| chat_id | session_id | user_id | timestamp | sender | message | detected_mood | model_used | song_recommended | song_selected |
|---|---|---|---|---|---|---|---|---|---|
| `bcb1f440-...` | `ecf4c0d3-...` | `08b1612a-...` | `00:25:58Z` | `user` | "I've had a really hard week, feeling exhausted and down." | `None` | `None` | `None` | `N` |
| `c94f6065-...` | `ecf4c0d3-...` | `08b1612a-...` | `00:25:59Z` | `bot` | "I hear you, Aarav. A relentless week takes a real toll... Let's listen to something gentle." | `sad` | `ollama/llama3.2` | `Fix You (Coldplay); Amake Amar Moto Thakte Dao (Anupam Roy); Kabira (Tochi Raina)` | `Y` |

### Sheet 4: `Music_Log`
| log_id | session_id | timestamp | song_title | artist | video_id | mood_at_time | user_selected |
|---|---|---|---|---|---|---|---|
| `8446d6ea-...` | `ecf4c0d3-...` | `00:25:58Z` | `Fix You` | `Coldplay` | `k4V3gHjgzjU` | `sad` | `N` |
| `6c7bc1ae-...` | `ecf4c0d3-...` | `00:25:58Z` | `Amake Amar Moto Thakte Dao` | `Anupam Roy` | `f5jF8jXkZ8g` | `sad` | `N` |
| `c43d4a43-...` | `ecf4c0d3-...` | `00:25:58Z` | `Kabira` | `Tochi Raina` | `jHNNMj5bNQw` | `sad` | `N` |
| `e1f82c40-...` | `ecf4c0d3-...` | `00:25:59Z` | `Fix You` | `Coldplay` | `k4V3gHjgzjU` | `sad` | `Y` |

### Sheet 5: `Feedback`
| feedback_id | session_id | user_id | timestamp | overall_rating | mood_before | mood_after | songs_helped | bot_understanding | model_rating | comments |
|---|---|---|---|---|---|---|---|---|---|---|
| `9752de60-...` | `ecf4c0d3-...` | `08b1612a-...` | `00:26:00Z` | 5 | `sad` | `calm` | `Yes` | 5 | 5 | "The music matched my mood gently without forcing fake happiness. Beautiful companion." |

---

## 6. Admin Data Decryption Utility (`admin_view.py`)

MoodMate includes a dedicated administrator CLI to view user records.

### View 1: Raw Mode (Proving Zero Plaintext PII Leakage)
```bash
python backend/admin_view.py --raw
```
Output:
```
==========================================================================================
 MoodMate Admin Viewer - Users Table (2 registered users)
==========================================================================================
[*] RAW MODE: Displaying un-decrypted stored ciphertext.

[1] User ID : 08b1612a-5361-4470-89f7-a8a5a78b6d14
    Email Hash  : 2de30c2aa84d...
    Name        : gAAAAABq6jVGGhS9EcnT...
    Email       : gAAAAABq6jVGNAkplKAZ...
    Phone       : gAAAAABq6jVGHXBCnUrm...
    Brain Model : gemini/gemini-2.0-flash
    Created At  : 2026-11-04T00:25:58Z
    Last Login  : 2026-11-04T00:25:58Z
```

### View 2: Authorized Decryption Mode (Using Master Key)
```bash
python backend/admin_view.py
```
Output:
```
==========================================================================================
 MoodMate Admin Viewer - Users Table (2 registered users)
==========================================================================================
[*] Master Fernet key loaded successfully. Decrypting PII fields...

[1] User ID : 08b1612a-5361-4470-89f7-a8a5a78b6d14
    Email Hash  : 2de30c2aa84d...
    Name        : Aarav Sen
    Email       : aarav.sen@example.com
    Phone       : +919876543210
    Brain Model : gemini/gemini-2.0-flash
    Created At  : 2026-11-04T00:25:58Z
    Last Login  : 2026-11-04T00:25:58Z
```

---

## 7. End-to-End Test Checklist

Use this checklist to verify complete functionality:

- [x] **Registration**: Validates email format, E.164 phone country code (`+91...`), password strength meter, and mandatory consent checkbox.
- [x] **Login**: Email + bcrypt verification; issue of signed JWT token.
- [x] **Model Picker**: Displays available models from `models.json` with privacy notices. Greys out unconfigured models.
- [x] **Session Start**: Greets user by first name, displays quick mood chips (😊 😐 😔 😡 😰 😴), records initial mood in `Sessions`.
- [x] **Chat Turn**: Bot detects mood (1-5 intensity), replies warmly, applies the **iso-principle**, and recommends 3 verified playable songs.
- [x] **Tappable Song Cards**: Clicking a card highlights it in green (`.now-playing-card`), updates the persistent bottom mini player, and starts streaming via YouTube IFrame API.
- [x] **Background Playback**: Mini player stays docked at bottom outside the chat container; audio continues without reloading or stuttering when new messages arrive.
- [x] **Mid-Session Brain Switch**: Switching the model mid-chat persists chat history and playback; announces "Switched chat brain to <model>" in chat.
- [x] **Server-Side Safety Trigger**: Pre- and post-LLM check scans crisis keywords in English, Hindi, Bengali, and Hinglish. Intercepts message, halts song recommendations, and returns 24/7 helplines.
- [x] **End Session & Feedback**: Captures 1–5 star rating, before/after mood, music helpfulness, understanding rating, and comments in `Feedback` sheet.
- [x] **Right to Be Forgotten**: Clicking "Delete My Account & All Data" purges user records from all 5 sheets (`Users`, `Sessions`, `Chats`, `Music_Log`, `Feedback`).

---

## 8. Note on Storage Scalability

MoodMate uses **Excel (.xlsx)** via `openpyxl` paired with `filelock` and an in-memory retry queue. This design makes the database portable and inspection-friendly without installing separate database software.

For larger deployments with high concurrent user loads, all storage methods are behind the `StorageInterface` in [`backend/storage.py`](file:///C:/Users/Nikhil%20Yadav/OneDrive/Desktop/MoodMate/backend/storage.py). You can swap `ExcelStorage` for an asynchronous SQLite or PostgreSQL storage class without touching any route, auth, or model logic.

