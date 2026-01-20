# modules/eyes.py
from droidrun import DroidAgent
import asyncio
import io
from PIL import Image

class ScreenEyes:
    def __init__(self, agent: DroidAgent):
        self.agent = agent

    async def capture_screenshot(self):
        """
        Captures screen asynchronously.
        Does not block the event loop while waiting for ADB data transfer.
        """
        try:
            # 1. Start the ADB process asynchronously
            process = await asyncio.create_subprocess_exec(
                "adb", "exec-out", "screencap", "-p",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # 2. Wait for data with a timeout (3 seconds)
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=3.0)
            except asyncio.TimeoutError:
                print(" [⚠️ ADB Timeout]", end="")
                try:
                    process.kill()
                except: 
                    pass
                return None

            if process.returncode == 0 and stdout:
                image_data = io.BytesIO(stdout)
                
                # 3. Open as PIL Image
                image = Image.open(image_data)
                
                # ⚡ HYPER-SPEED OPTIMIZATION ⚡
                # Resize to 256px. 
                # This is ~75% smaller than 480px and uploads instantly.
                image.thumbnail((256, 256)) 
                
                return image
                
            return None
        except Exception as e:
            # Silently fail on errors to keep the loop running
            return None

    def get_current_app_component(self):
        """
        Fast check for the active app package.
        (Kept synchronous as it is very fast and low-overhead)
        """
        import subprocess # Local import to avoid confusion
        try:
            cmd = "adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'"
            # Reduced timeout to 0.5s to keep the loop tight
            result = subprocess.check_output(cmd, shell=True, timeout=0.5).decode('utf-8')
            if "/" in result:
                tokens = result.split()
                for token in tokens:
                    if "/" in token and "}" not in token:
                        return token.strip()
            return None
        except Exception:
            return None