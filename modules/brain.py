import google.generativeai as genai
from .config import Config
import traceback

class AcademicBrain:
    def __init__(self):
        genai.configure(api_key=Config.API_KEY)
        # Uses the model defined in Config, default to 1.5-flash if missing
        model_name = getattr(Config, 'MODEL_NAME', 'gemini-1.5-flash')
        self.model = genai.GenerativeModel(model_name)

    async def judge_image(self, image_input):
        if image_input is None:
            return False

        # We inject the goal, but we wrap it in a "Broad Academic" context.
        prompt = (
            f"CURRENT USER GOAL: '{Config.USER_GOAL}'\n\n"
            
            "--- 🎓 ACADEMIC MONITOR INSTRUCTIONS ---\n"
            "You are a strict but intelligent study supervisor. Your job is to classify the user's screen activity.\n"
            "The User's Goal above indicates their **Subject of Study**, but their **Method of Study** is dynamic.\n\n"
            
            "✅ VERDICT: PRODUCTIVE (Allow these)\n"
            "1. **Any Learning Format**: The user might switch from a Video Lecture to a PDF, a Slide Deck, a Wikipedia article, or a documentation site. This is NORMAL.\n"
            "2. **Tools & Reference**: Code Editors (VS Code), Terminals, Calculators, Excel, StackOverflow, GeeksForGeeks, or University Portals.\n"
            "3. **General Organization**: File Explorer, Calendar, or Note-taking apps (Notion, Obsidian).\n"
            "4. **Subject Relevance**: If the goal is 'Physics', a PDF about 'Math' is arguably still productive. Give the benefit of the doubt for *any* academic text.\n\n"

            "⛔ VERDICT: DISTRACTION (Block these)\n"
            "1. **Entertainment**: Netflix, Prime Video, Anime sites, Cartoons, Movies.\n"
            "2. **Social Media**: Instagram Reels, TikTok, Twitter/X Feeds, Facebook, Discord Chat (unless clearly technical).\n"
            "3. **Gaming**: Any game visuals, HUDs, Steam store, Twitch streams.\n"
            "4. **Off-Topic Video**: If the user is on YouTube, look at the video title. If it is Music Videos, Vlogs, Gaming, or Gossip -> DISTRACTION. (Educational YouTube is OK).\n\n"
            
            "--- 🧠 DECISION LOGIC ---\n"
            "- Does the screen look like work/study (text-heavy, diagrams, code)? -> PRODUCTIVE\n"
            "- Does the screen look like fun (colorful thumbnails, infinite scroll, chat bubbles)? -> DISTRACTION\n"
            "- IGNORE format mismatches. If the goal says 'Watch Video' but they are reading a 'PDF', that is PRODUCTIVE.\n\n"

            "OUTPUT STRICTLY ONE WORD: 'DISTRACTION' or 'PRODUCTIVE'"
        )
        
        try:
            # Generate response
            response = self.model.generate_content([prompt, image_input])
            
            if not response.text:
                print(" [⚠️ Brain Error: Empty Response]")
                return False

            verdict_text = response.text.strip().upper()
            
            # Debug output (Visible to you)
            print(f" [👁️ AI Verdict: {verdict_text}]", end="")
            
            # Return True only if clearly distracted
            return "DISTRACTION" in verdict_text
            
        except Exception as e:
            print(f"\n❌ BRAIN FAILURE: {e}")
            return False