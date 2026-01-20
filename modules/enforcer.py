from droidrun import DroidAgent
import os
import time
import asyncio
import shlex 
from .config import Config

class PoliceOfficer:
    def __init__(self, agent: DroidAgent, resource_manager):
        self.agent = agent
        self.resources = resource_manager

    async def _agentic_whatsapp_search(self):
        target_name = Config.RECIPIENT_NAME
        if not target_name:
            return

        print(f"🐀 AGENT: Opening WhatsApp to report to '{target_name}'...")
        
        # 1. Open WhatsApp Home
        os.system("adb shell am start -n com.whatsapp/.Main")
        await asyncio.sleep(2.0)
        
        # 2. Search
        os.system("adb shell input keyevent 84") 
        await asyncio.sleep(1.0)
        
        # 3. Type Name
        safe_name = shlex.quote(target_name)
        os.system(f"adb shell input text {safe_name}")
        await asyncio.sleep(1.5)
        
        # 4. Select Result
        os.system("adb shell input keyevent 20") # Down
        await asyncio.sleep(0.2)
        os.system("adb shell input keyevent 66") # Enter
        await asyncio.sleep(2.0)
        
        # 5. Type Message
        msg = f"I%sAM%sDISTRACTED.%sGOAL:%sFAILED"
        os.system(f"adb shell input text {msg}")
        await asyncio.sleep(0.5)
        
        # 6. SEND FIX 
        print("   (Navigating to Send button...)")
        
        # TAB 1: Focus moves from Text Box -> Attachment Clip
        os.system("adb shell input keyevent 61") 
        await asyncio.sleep(0.1)
        
        # TAB 2: Focus moves from Attachment Clip -> Camera/Send Button
        # (We add this second TAB to skip the clip)
        os.system("adb shell input keyevent 61") 
        await asyncio.sleep(0.1)
        
        # ENTER: Click the highlighted button (Send)
        os.system("adb shell input keyevent 66") 
        await asyncio.sleep(0.5)

    async def _show_browser_popup(self, message_text):
        print(f"📢 WARNING: {message_text}")
        query = message_text.replace(" ", "+")
        cmd = f'adb shell am start -a android.intent.action.VIEW -d "https://www.google.com/search?q={query}" > /dev/null 2>&1'
        os.system(cmd)

    async def soft_correction(self):
        print(f"👮 POLICE: Warning Strike.")
        os.system("adb shell input keyevent 3") 
        await self._show_browser_popup("STRIKE_WARNING_GO_STUDY")

    async def force_reset(self):
        print("👮 POLICE: Distraction Warning.")
        os.system("adb shell input keyevent 127") 
        await asyncio.sleep(0.2)
        os.system("adb shell input keyevent 3") 
        await self._show_browser_popup("FOCUS_ON_YOUR_GOAL")

    async def play_penalty_gif(self):
        print("🚨🚨 MAX STRIKES! AGENT TAKING CONTROL 🚨🚨")
        
        # 1. Play GIF
        local_path = self.resources.get_image_path('penalty.gif')
        remote_path = "/sdcard/Download/penalty.gif"
        if os.path.exists(local_path):
            os.system(f'adb push "{local_path}" "{remote_path}" > /dev/null 2>&1')
            time.sleep(0.5)
            file_url = f"file://{remote_path}"
            os.system(f'adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d "{file_url}" > /dev/null 2>&1')
            await asyncio.sleep(4) 
            
        # 2. Snitch
        await self._agentic_whatsapp_search()
        
        # 3. Home
        await asyncio.sleep(1)
        os.system("adb shell input keyevent 3")