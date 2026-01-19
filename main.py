import asyncio
import time
import logging

logging.getLogger("droidrun").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

from droidrun import DroidAgent, DroidrunConfig, AgentConfig, DeviceConfig
from modules.config import Config
from modules.eyes import ScreenEyes
from modules.brain import AcademicBrain
from modules.enforcer import PoliceOfficer
from modules.resource_manager import ResourceManager

async def main():
    print(f"--- 🛡️ Focus-Flow Pro: Vision Edition ---")
    
    # 1. SETUP
    print("\n" + "="*50)
    user_input = input("👉 Enter Task (e.g. 'Study Computer Architecture'): ")
    if user_input.strip(): Config.USER_GOAL = user_input
    print(f"✅ GOAL LOCKED: {Config.USER_GOAL}")
    print("="*50 + "\n")

    droid_config = DroidrunConfig(
        agent=AgentConfig(max_steps=10000), 
        device=DeviceConfig(platform="android")
    )
    base_agent = DroidAgent(goal="System", config=droid_config, llms={})
    resources = ResourceManager()
    eyes = ScreenEyes(base_agent)
    brain = AcademicBrain()
    police = PoliceOfficer(base_agent, resources)

    # --- 🔎 SYSTEM CHECK ---
    print("🛠️  PERFORMING SYSTEM CHECK...")
    test_shot = eyes.capture_screenshot()
    if test_shot:
        print("📸 Camera: ONLINE")
        print("🧠 Connecting to Brain...")
        is_distracted = await brain.judge_image(test_shot)
        verdict = "DISTRACTION" if is_distracted else "PRODUCTIVE"
        print(f"✅ System Check Complete. Initial Verdict: {verdict}")
        test_shot.close()
    else:
        print("❌ CRITICAL: Camera Failed. Check ADB Connection.")
    print("   (Monitoring started. Printing '.' for every scan)")
    print("-" * 50)
    # -----------------------

    strike_counter = 0
    last_smart_check = 0
    
    while True:
        # A. FAST CHECKS
        current_component = eyes.get_current_app_component()
        current_package = current_component.split('/')[0] if current_component else ""
        
        is_in_safe_zone = False
        if current_package:
            for safe_app in Config.SAFE_PACKAGES:
                if safe_app in current_package:
                    is_in_safe_zone = True
                    break
        
        # Simple Package Ban Check
        wrong_app_detected = False
        if current_package:
            for ban_keyword in Config.BANNED_APPS_KEYWORDS:
                if ban_keyword.lower() in current_package.lower():
                    wrong_app_detected = True
                    print(f"\n🚨 BANNED APP DETECTED: {current_package}")
                    break

        just_punished = False

        if wrong_app_detected:
            # --- FIXED: LOGIC ALREADY EXISTED HERE ---
            print(f"\n🚨 BANNED APP: {wrong_app_detected}")
            strike_counter += 1
            if strike_counter >= Config.MAX_STRIKES:
                await police.play_penalty_gif()
                strike_counter = 0
            else:
                await police.hard_correction()
            just_punished = True
            
        elif not is_in_safe_zone and current_package != "" and "launcher" not in current_package:
             pass 

        # B. VISION CHECK
        if not just_punished and (time.time() - last_smart_check > Config.POLLING_RATE_SMART):
            
            print(".", end="", flush=True) 
            
            screenshot = eyes.capture_screenshot()
            
            if screenshot:
                is_distracted = await brain.judge_image(screenshot)
                
                if is_distracted:
                    print("\n⛔ VISION VERDICT: DISTRACTION DETECTED.")
                    strike_counter += 1
                    
                    # --- FIXED: ADDED MAX STRIKE CHECK HERE ---
                    if strike_counter >= Config.MAX_STRIKES:
                        await police.play_penalty_gif()
                        strike_counter = 0
                    else:
                        await police.force_reset()
                    # ------------------------------------------
                    
                    just_punished = True
                
                screenshot.close()
            
            last_smart_check = time.time()

        if just_punished:
            print("\n🛡️  GRACE PERIOD: 5 seconds...")
            await asyncio.sleep(5)
            print("👀 Resuming watch.\n")
            continue

        await asyncio.sleep(Config.POLLING_RATE_FAST)

if __name__ == "__main__":
    asyncio.run(main())