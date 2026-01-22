import google.generativeai as genai
from .config import Config

class AcademicBrain:
    def __init__(self):
        genai.configure(api_key=Config.API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def judge_image(self, image):
        if image is None:
            return False

        prompt = (
            f"USER GOAL: {Config.USER_GOAL}\n"
            "Classify screen as PRODUCTIVE or DISTRACTION.\n"
            "Return ONE WORD."
        )

        try:
            response = await self.model.generate_content_async([prompt, image])
            verdict = response.text.strip().upper()
            print(f" [👁️ AI Verdict: {verdict}]")
            return "DISTRACTION" in verdict
        except:
            return False
