from llama_index.llms.google_genai import GoogleGenAI
from .config import Config

class AcademicBrain:
    def __init__(self):
        self.llm = GoogleGenAI(
            model=Config.MODEL_NAME, 
            api_key=Config.API_KEY,
            temperature=0.0 # Zero creativity = Strict rules
        )

    async def judge_content(self, screen_text):
        """
        Asks Gemini: Is the MAIN CONTENT relevant?
        """
        prompt = (
            f"USER GOAL: {Config.CURRENT_GOAL}\n"
            f"SCREEN CONTEXT: {screen_text}\n\n"
            "ROLE: You are a Strict Productivity Police Officer.\n\n"
            "CONTEXT (YOUTUBE MODE):\n"
            "The screen contains a Main Video (Active) and Recommended Videos (Sidebar).\n"
            "You must detect if the MAIN VIDEO is a distraction.\n\n"
            "🚨 IMMEDIATE BAN (SAY 'NO') IF YOU SEE:\n"
            "1. GAMING TERMS: 'Gameplay', 'Walkthrough', 'Let\'s Play', 'Live Stream', 'Ranked', 'Boss Fight', 'Minecraft', 'Roblox', 'PUBG', 'Clash', 'Valorant', 'GTA'.\n"
            "2. ENTERTAINMENT: 'Prank', 'Reaction', 'Vlog', 'Challenge', 'Highlights', 'Movie Scene', 'Trailer'.\n"
            "3. MUSIC: 'Official Video', 'Lyrics', 'Music Video'.\n"
            "4. If the text is mostly empty/short but contains 'Level', 'XP', 'Ammo', 'Map' -> It is a game -> SAY 'NO'.\n\n"
            "✅ PASS (SAY 'YES') ONLY IF:\n"
            "1. You see explicit educational keywords: 'Lecture', 'Tutorial', 'Course', 'Python', 'Math', 'Physics', 'History', 'Documentary'.\n"
            "2. The screen is JUST System UI (e.g., 'Home', 'Search', 'Library', 'Settings') with NO gaming terms.\n\n"
            "⚡ THE GOLDEN RULE:\n"
            "- If you see 'Calculus' AND 'Minecraft' on screen -> ASK YOURSELF: Is 'Minecraft' the title? If unsure, but 'Calculus' is present, say YES (Safe).\n"
            "- If you see 'Minecraft' and NO educational words -> SAY NO (Distraction).\n"
            "- If you are watching Gameplay, the verdict MUST be NO.\n\n"
            "VERDICT (Answer strictly with one word: YES or NO):"
        )
        
        try:
            response = await self.llm.acomplete(prompt)
            verdict = response.text.strip().upper()
            
            print(f"      [🧠 AI Thought: {verdict}]")
            
            # Logic: If AI says "NO", it means NOT PRODUCTIVE -> Distraction.
            return "NO" in verdict 
            
        except Exception as e:
            print(f"⚠️ Brain Freeze: {e}")
            return False