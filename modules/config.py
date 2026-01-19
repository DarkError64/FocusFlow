import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("❌ API Key not found! Check .env file.")

    MODEL_NAME = "models/gemini-2.5-flash" 
    
    POLLING_RATE_FAST = 0.5
    POLLING_RATE_SMART = 4.0 # Slightly faster AI checks
    MAX_STRIKES = 3
    
    # This will be overwritten by user input at startup
    USER_GOAL = "General Productivity" 

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
    
    # We still keep the "Hard Ban" list for obvious non-productive apps
    BANNED_APPS_KEYWORDS = [
        "Instagram", "TikTok", "Snapchat", "Facebook", "Discord", "Reddit", "Threads",
        "Netflix", "Prime Video", "Disney+", "Hotstar", "Twitch", "Spotify", 
        "Clash", "PUBG", "BGMI", "Free Fire", "Candy Crush", "Roblox"
    ]
    
    # Short triggers for fast detection
    IN_APP_TRIGGERS = ["Shorts", "Reels", "Remix", "Suggested for you", "Trending", "Explore"]