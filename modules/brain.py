import os
import sys

# 1. MUTE DEPRECATION WARNINGS
# We temporarily redirect errors to "nowhere" while importing
_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

import google.generativeai as genai

# Restore error logging
sys.stderr = _stderr

from .config import Config
import warnings

# Keep these filters just in case
warnings.filterwarnings("ignore")

class AcademicBrain:
    def __init__(self):
        genai.configure(api_key=Config.API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def judge_image(self, image_input):
        """
        Universal Distraction Detection.
        """
        if image_input is None:
            return False

        prompt = (
            f"USER'S STATED GOAL: '{Config.USER_GOAL}'\n"
            "TASK: You are a strict Productivity Officer. Determine if the user is working or slacking off.\n\n"
            "--- 🛡️ THE PRODUCTIVITY WHITELIST (SAFE) ---\n"
            "The user is ONLY allowed to be doing these things. Mark as PRODUCTIVE if you see:\n"
            "1. **Educational Content**: Lectures, Tutorials, Whiteboards, Slide Presentations.\n"
            "2. **Reading/Writing**: PDFs, Text Documents, Notes, Articles, Books, Wikipedia.\n"
            "3. **Technical Work**: Code Editors (VS Code), Terminals, Excel/Sheets, Calculator.\n"
            "4. **System Navigation**: Home Screen, File Explorer, App Library (Transitioning).\n\n"
            "--- 🚨 THE UNIVERSAL BLOCKLIST (UNSAFE) ---\n"
            "ANYTHING that does not fit the list above is a DISTRACTION.\n"
            "Common examples: Games, Social Media, Movies, Gossip/News.\n\n"
            "OUTPUT STRICTLY ONE WORD: DISTRACTION or PRODUCTIVE"
        )
        
        try:
            # Using the async method (Performance Fix)
            response = await self.model.generate_content_async([prompt, image_input])
            
            if not response.text:
                return False

            verdict = response.text.strip().upper()
            
            # 3. PRINT ON NEW LINE
            # Removed 'end=""' so every verdict gets its own line
            print(f" [👁️ AI Verdict: {verdict}]") 
            
            return "DISTRACTION" in verdict
            
        except Exception as e:
            print(f" [⚠️ Error: {e}]")
            return False