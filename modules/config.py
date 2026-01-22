import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("❌ API Key not found!")

    MODEL_NAME = "models/gemini-2.5-flash"

    POLLING_RATE_FAST = 0.5
    POLLING_RATE_SMART = 4.0
    MAX_STRIKES = 3

    # ⏳ TIMERS
    STARTUP_COOLDOWN = 10
    GRACE_PERIOD = 8

    USER_GOAL = "General Productivity"
    RECIPIENT_NAME = None

    SAFE_PACKAGES = [
        "com.google.android.youtube",
        "com.google.android.apps.docs",
        "com.adobe.reader",
        "com.google.android.apps.docs.editors.docs",
        "com.google.android.apps.docs.editors.sheets",
        "com.microsoft.office.word",
        "com.android.chrome",
        "org.mozilla.firefox",
        "com.google.android.apps.nbu.files"
    ]

    BANNED_APPS_KEYWORDS = [
        "Instagram", "TikTok", "Snapchat", "Facebook", "Discord", "Reddit",
        "Netflix", "Prime Video", "Hotstar", "Twitch", "Spotify",
        "PUBG", "BGMI", "Free Fire", "Candy Crush", "Roblox"
    ]

    IN_APP_TRIGGERS = ["Shorts", "Reels", "Explore"]
