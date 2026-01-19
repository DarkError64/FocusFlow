from droidrun import DroidAgent
import subprocess
import io
from PIL import Image

class ScreenEyes:
    def __init__(self, agent: DroidAgent):
        self.agent = agent

    def capture_screenshot(self):
        """
        Captures screen strictly to RAM via ADB pipe.
        Stealth Mode: No file is created on the Android device.
        """
        try:
            # 'exec-out' writes binary to stdout, skipping file storage
            result = subprocess.run(
                ["adb", "exec-out", "screencap", "-p"], 
                capture_output=True,
                timeout=6  # Increased slightly for high-res screens
            )
            
            if result.returncode == 0 and result.stdout:
                image_data = io.BytesIO(result.stdout)
                image = Image.open(image_data)
                # Resize to speed up upload to Gemini (stealthier bandwidth usage)
                image.thumbnail((1024, 1024)) 
                return image
            return None
        except subprocess.TimeoutExpired:
            print("⚠️ Camera Timeout (Phone busy or ADB disconnected)")
            return None
        except Exception as e:
            print(f"❌ Camera Error: {e}")
            return None

    def get_current_app_component(self):
        """
        Fast, lightweight check for the active app package.
        """
        try:
            cmd = "adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'"
            result = subprocess.check_output(cmd, shell=True, timeout=2).decode('utf-8')
            if "/" in result:
                tokens = result.split()
                for token in tokens:
                    if "/" in token and "}" not in token:
                        return token.strip()
            return None
        except Exception:
            return None