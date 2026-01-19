import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("❌ API Key not found! Check .env file.")

    MODEL_NAME = "models/gemini-2.5-flash" 
    
    POLLING_RATE_FAST = 0.5
    POLLING_RATE_SMART = 5.0
    MAX_STRIKES = 3
    
    # --- SAFE ZONE WHITELIST ---
    # These apps are ALWAYS allowed (Multitasking enabled)
    SAFE_PACKAGES = [
        "com.google.android.youtube",          # YouTube
        "com.google.android.apps.docs",        # Google Drive
        "com.adobe.reader",                    # Adobe Acrobat
        "com.google.android.apps.docs.editors.docs", # Google Docs
        "com.google.android.apps.docs.editors.sheets", # Sheets
        "com.microsoft.office.word",           # MS Word
        "com.android.chrome",                  # Chrome
        "org.mozilla.firefox",                 # Firefox
        "com.google.android.apps.nbu.files"    # Files by Google
    ]

    CURRENT_GOAL = "Studying Physics, Math, Coding, or Reading Academic Papers."
    
    IN_APP_TRIGGERS = ["Shorts", "Reels", "Remix", "Suggested for you", "Trending", "Explore", "Live", "Gaming"]

    BANNED_APPS_KEYWORDS = [
        "Instagram", "TikTok", "Snapchat", "Facebook", "Twitter", "Discord", "Reddit", "Threads",
        "Netflix", "Prime Video", "Disney+", "Hotstar", "Twitch", "Spotify", "Zee5",
        "Clash", "PUBG", "BGMI", "Free Fire", "Candy Crush", "Roblox", "Game Launcher"
    ]