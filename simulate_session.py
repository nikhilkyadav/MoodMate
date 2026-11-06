"""
simulate_session.py - Runs a complete end-to-end simulated session for MoodMate,
populating moodmate_data.xlsx with realistic user data, chats, music logs, and feedback.
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from backend.crypto import get_crypto_manager
from backend.storage import get_storage
from backend.music import get_music_engine
from backend.safety import check_crisis_text, build_crisis_response
import asyncio

async def run_simulation():
    print("=" * 70)
    print(" MoodMate - Live Session Simulation")
    print("=" * 70)

    storage = get_storage()
    crypto = get_crypto_manager()
    music = get_music_engine()

    # 1. Register User
    user_id = str(uuid.uuid4())
    raw_name = "Aarav Sen"
    raw_email = "aarav.sen@example.com"
    raw_phone = "+919876543210"
    raw_pass = "AaravEmpathetic!2026"
    email_hash = crypto.hash_email(raw_email)

    now = datetime.now(timezone.utc).isoformat()
    user_record = {
        "user_id": user_id,
        "email_hash": email_hash,
        "name_enc": crypto.encrypt(raw_name),
        "email_enc": crypto.encrypt(raw_email),
        "phone_enc": crypto.encrypt(raw_phone),
        "password_hash": crypto.hash_password(raw_pass),
        "preferred_model": "ollama/llama3.2",
        "created_at": now,
        "last_login": now
    }
    storage.create_user(user_record)
    print(f"[OK] Registered user: '{raw_name}' ({raw_email})")
    print(f"    Encrypted Name  : {user_record['name_enc'][:24]}...")
    print(f"    Encrypted Email : {user_record['email_enc'][:24]}...")
    print(f"    Encrypted Phone : {user_record['phone_enc'][:24]}...")
    print(f"    HMAC Email Hash : {email_hash[:16]}...")

    # 2. Start Session
    session_id = str(uuid.uuid4())
    session_start = datetime.now(timezone.utc).isoformat()
    storage.create_session({
        "session_id": session_id,
        "user_id": user_id,
        "start_time": session_start,
        "end_time": "",
        "initial_mood": "sad",
        "final_mood": "",
        "songs_played_count": 0,
        "models_used": "ollama/llama3.2"
    })
    print(f"\n[OK] Started Session: {session_id} (Initial Mood: sad)")

    # 3. Chat Turn 1: User vents
    user_msg_1 = "I've had a really hard week, feeling exhausted and down. Work was overwhelming."
    chat_id_1 = str(uuid.uuid4())
    storage.log_chat({
        "chat_id": chat_id_1,
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sender": "user",
        "message": user_msg_1,
        "detected_mood": "",
        "model_used": "",
        "song_recommended": "",
        "song_selected": "N"
    })

    # Bot Turn 1: Empathetic reply + iso-principle song recommendations
    bot_reply_1 = (
        "I hear you, Aarav. A relentless week takes a real toll on your spirit, "
        "and it makes total sense that you're feeling down right now. You don't have to carry "
        "all of that alone. Let's listen to something gentle together that honors how you're feeling."
    )
    recs_1 = await music.resolve_song_recommendations([
        {"title": "Fix You", "artist": "Coldplay", "language": "English", "reason": "Starts in quiet grief and builds into healing."},
        {"title": "Amake Amar Moto Thakte Dao", "artist": "Anupam Roy", "language": "Bengali", "reason": "Quiet solace when the world is too loud."},
        {"title": "Kabira", "artist": "Tochi Raina & Rekha Bhardwaj", "language": "Hindi", "reason": "Soulful comfort and gentle acceptance."}
    ], current_mood="sad")

    titles_str_1 = "; ".join([f"{s['title']} ({s['artist']})" for s in recs_1])
    bot_chat_id_1 = str(uuid.uuid4())
    storage.log_chat({
        "chat_id": bot_chat_id_1,
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sender": "bot",
        "message": bot_reply_1,
        "detected_mood": "sad",
        "model_used": "ollama/llama3.2",
        "song_recommended": titles_str_1,
        "song_selected": "N"
    })

    # Log recommendations to Music_Log
    for s in recs_1:
        storage.log_music({
            "log_id": str(uuid.uuid4()),
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "song_title": s["title"],
            "artist": s["artist"],
            "video_id": s["video_id"],
            "mood_at_time": "sad",
            "user_selected": "N"
        })
    print(f"[OK] Logged User Message & Bot Response with 3 Iso-Principle Recommendations:")
    for idx, s in enumerate(recs_1, 1):
        print(f"    Card {idx}: '{s['title']}' by {s['artist']} [YouTube: {s['video_id']}]")

    # 4. User Selects Song 1 (Fix You)
    selected_song = recs_1[0]
    storage.log_music({
        "log_id": str(uuid.uuid4()),
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "song_title": selected_song["title"],
        "artist": selected_song["artist"],
        "video_id": selected_song["video_id"],
        "mood_at_time": "sad",
        "user_selected": "Y"
    })
    storage.update_chat_song_selection(session_id, selected_song["title"])
    print(f"[OK] User selected: '{selected_song['title']}' -> Marked song_selected='Y'")

    # 5. Mid-Session Model Switch
    storage.update_user_model(user_id, "gemini/gemini-2.0-flash")
    print("[OK] Mid-session model switched to: gemini/gemini-2.0-flash")

    # 6. Safety Trigger Check Turn
    crisis_input = "Sometimes I feel like I just want to kill myself, I can't take this pain."
    is_crisis, kw = check_crisis_text(crisis_input)
    print(f"\n[OK] Testing Server-Side Crisis Interception for: '{crisis_input}'")
    print(f"    Crisis Matched: {is_crisis} (Keyword: '{kw}')")

    crisis_resp = build_crisis_response("Aarav")
    storage.log_chat({
        "chat_id": str(uuid.uuid4()),
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sender": "user",
        "message": crisis_input,
        "detected_mood": "",
        "model_used": "",
        "song_recommended": "",
        "song_selected": "N"
    })
    storage.log_chat({
        "chat_id": str(uuid.uuid4()),
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sender": "bot",
        "message": crisis_resp["reply"],
        "detected_mood": "crisis",
        "model_used": "gemini/gemini-2.0-flash",
        "song_recommended": "",
        "song_selected": "N"
    })
    print("[OK] Crisis safety response logged with zero songs and 24/7 confidential helplines.")

    # 7. End Session & Feedback
    session_end = datetime.now(timezone.utc).isoformat()
    storage.end_session(
        session_id=session_id,
        end_time=session_end,
        final_mood="calm",
        songs_played_count=1,
        models_used="ollama/llama3.2, gemini/gemini-2.0-flash"
    )

    feedback_id = str(uuid.uuid4())
    storage.log_feedback({
        "feedback_id": feedback_id,
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": session_end,
        "overall_rating": 5,
        "mood_before": "sad",
        "mood_after": "calm",
        "songs_helped": "Yes",
        "bot_understanding": 5,
        "model_rating": 5,
        "comments": "The music matched my mood gently without forcing fake happiness. Beautiful companion."
    })
    print("[OK] Session ended and Feedback logged (Rating: 5/5, Mood: sad -> calm).")

    print("\n" + "=" * 70)
    print(" Simulation Complete! Excel file 'moodmate_data.xlsx' is fully populated.")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_simulation())
