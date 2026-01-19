from droidrun import DroidAgent
import subprocess
import os

class ScreenEyes:
    def __init__(self, agent: DroidAgent):
        self.agent = agent

    async def scan(self):
        """
        Captures screen text using Raw ADB.
        """
        try:
            # Dump UI hierarchy
            subprocess.run("adb shell uiautomator dump /sdcard/window_dump.xml", shell=True, timeout=5, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            # Read the text
            result = subprocess.check_output("adb shell cat /sdcard/window_dump.xml", shell=True).decode('utf-8')
            return result.lower()
        except Exception:
            # If dump fails, return empty string
            return ""

    def get_current_app_component(self):
        """
        Finds the active package/activity.
        """
        try:
            cmd = "adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'"
            result = subprocess.check_output(cmd, shell=True).decode('utf-8')
            
            # Parse output: "mCurrentFocus=Window{... u0 com.package/activity ...}"
            if "/" in result:
                tokens = result.split()
                for token in tokens:
                    if "/" in token and "}" not in token:
                        return token.strip()
            return None
        except Exception:
            return None

    def detects_distraction(self, screen_text, triggers):
        """
        Simple keyword search.
        """
        if not screen_text:
            return None
        for trigger in triggers:
            if trigger.lower() in screen_text:
                return trigger
        return None