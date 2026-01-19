from droidrun import DroidAgent
import os
import time
import asyncio
from .config import Config

class PoliceOfficer:
    def __init__(self, agent: DroidAgent, resource_manager):
        self.agent = agent
        self.resources = resource_manager

    async def _show_browser_popup(self, message_text):
        """Opens a Google Search with the warning text."""
        print(f"📢 WARNING: {message_text}")
        query = message_text.replace(" ", "+")
        cmd = f'adb shell am start -a android.intent.action.VIEW -d "https://www.google.com/search?q={query}" > /dev/null 2>&1'
        os.system(cmd)
        await asyncio.sleep(2.5)
        os.system("adb shell input keyevent 3") # Go Home

    async def soft_correction(self):
        print(f"👮 POLICE: Soft correction (Back Button).")
        os.system("adb shell input keyevent 4")

    async def force_reset(self):
        """
        Standard Punishment: Pause -> Home -> Specific Warning.
        """
        print("👮 POLICE: Goal Deviation Detected! Resetting...")
        
        # 1. Pause Video
        os.system("adb shell input keyevent 127")
        time.sleep(0.2)
        os.system("adb shell input keyevent 127")
        time.sleep(0.5)
        
        # 2. Go Home
        os.system("adb shell input keyevent 3")
        
        # 3. Show Specific Instruction
        # We use the search bar hack because it is reliable.
        await self._show_browser_popup("OPEN_LECTURE_VIDEO_AND_STUDY")

    async def hard_correction(self):
        """Wrong App Punishment"""
        print(f"👮 POLICE: Wrong App! Go Home.")
        os.system("adb shell input keyevent 3")
        await self._show_browser_popup("OPEN_LECTURE_VIDEO_AND_STUDY")

    async def play_penalty_gif(self):
        print("🚨🚨 MAX STRIKES! 🚨🚨")
        # Silence
        os.system("adb shell input keyevent 127")
        time.sleep(0.2)
        
        local_path = self.resources.get_image_path('penalty.gif')
        remote_path = "/sdcard/Download/penalty.gif"
        
        if os.path.exists(local_path):
            os.system(f'adb push "{local_path}" "{remote_path}" > /dev/null 2>&1')
            time.sleep(0.5)
            
            # Play GIF
            file_url = f"file://{remote_path}"
            os.system(f'adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d "{file_url}" > /dev/null 2>&1')
            
            await asyncio.sleep(6)
            os.system("adb shell input keyevent 3")
            
            # Final Warning
            await self._show_browser_popup("GET_BACK_TO_WORK")