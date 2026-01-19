from droidrun import DroidAgent
import os
import time
import asyncio
import subprocess
from .config import Config

class PoliceOfficer:
    def __init__(self, agent: DroidAgent, resource_manager):
        self.agent = agent
        self.resources = resource_manager

    async def _show_browser_popup(self, message_text):
        """
        Opens Google Search to display a message.
        """
        print(f"📢 POPUP: {message_text}")
        query = message_text.replace(" ", "+")
        cmd = f'adb shell am start -a android.intent.action.VIEW -d "https://www.google.com/search?q={query}" > /dev/null 2>&1'
        os.system(cmd)
        await asyncio.sleep(3.0)
        os.system("adb shell input keyevent 3")

    async def soft_correction(self):
        """In-App Correction (Back Button)"""
        print(f"👮 POLICE: Soft correction (Back Button).")
        os.system("adb shell input keyevent 4")

    async def force_reset(self):
        """
        For Irrelevant Video.
        Action: Heavy Pause -> Home -> Popup -> 5s Countdown.
        """
        print("👮 POLICE: Irrelevant Video! Pausing and Resetting...")
        
        # 1. PAUSE (The "Anti-PiP" Sequence)
        os.system("adb shell input keyevent 127")
        time.sleep(0.2)
        os.system("adb shell input keyevent 127")
        time.sleep(1.0) # Wait for app to realize it's paused
        
        # 2. GO HOME
        os.system("adb shell input keyevent 3")
        time.sleep(0.5)
        
        # 3. PAUSE AGAIN (Kill PiP)
        os.system("adb shell input keyevent 127")
        
        # 4. SHOW POPUP
        await self._show_browser_popup("⛔_OPEN_YOUR_STUDY_APP_NOW_⛔")
        
        # 5. VISIBLE TIMER
        print("\n" + "!"*40)
        print("⏳ PENALTY BOX ACTIVATED")
        for i in range(5, 0, -1):
            print(f"   ▶️  Resume possible in {i} seconds...", end="\r")
            time.sleep(1)
        print("\n✅ Time up.\n")

    async def hard_correction(self):
        """For Wrong App (Instagram)."""
        print(f"👮 POLICE: Wrong App! Go Home.")
        os.system("adb shell input keyevent 3")
        time.sleep(0.5)
        os.system("adb shell input keyevent 127") # Kill background audio
        await self._show_browser_popup("⚠️_DISTRACTION_DETECTED_GO_STUDY_⚠️")

    async def play_penalty_gif(self):
        print("🚨🚨 MAX STRIKES! 🚨🚨")
        
        # --- NEW: SILENCE THE DISTRACTION FIRST ---
        print("🔇 Silencing Audio...")
        os.system("adb shell input keyevent 127") # Pause Media
        time.sleep(0.2)
        os.system("adb shell input keyevent 127") # Double tap to be sure
        # ------------------------------------------

        local_path = self.resources.get_image_path('penalty.gif')
        remote_path = "/sdcard/Download/penalty.gif"
        
        if os.path.exists(local_path):
            # 1. Push GIF
            os.system(f'adb push "{local_path}" "{remote_path}" > /dev/null 2>&1')
            time.sleep(0.5)
            
            # 2. Play GIF in Chrome
            print("🎞️ Playing GIF in Chrome...")
            file_url = f"file://{remote_path}"
            os.system(f'adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d "{file_url}" > /dev/null 2>&1')
            
            # 3. Wait 6 seconds (Shame Duration)
            await asyncio.sleep(6)
            
            # 4. Clean up: Go Home
            os.system("adb shell input keyevent 3")
            
            # 5. Show Final Warning Popup
            await self._show_browser_popup("❌_STRIKE_LIMIT_REACHED_❌")
        else:
            print(f"❌ Error: GIF not found at {local_path}")