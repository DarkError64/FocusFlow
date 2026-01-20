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
    print(f"\n--- 🛡️ Focus-Flow Pro: Agent Edition ---")
    
    # --- 1. SESSION SETUP ---
    print("="*50)
    
    # 2. HARDCODED GOAL (No user input requested)
    Config.USER_GOAL = "Studying"
    print(f"👉 Task Auto-Set : {Config.USER_GOAL}")
    
    print("\n👮 ACCOUNTABILITY SETUP")
    contact_name = input("👉 Enter Contact Name : ").strip()
    
    if contact_name:
        Config.RECIPIENT_NAME = contact_name
        print(f"✅ Snitch Target Set: '{Config.RECIPIENT_NAME}'")
    else:
        print("⚠️ No name entered. Social penalties disabled.")
            
    print("="*50 + "\n")

    # Initialize Agents
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
    test_shot = await eyes.capture_screenshot()
    if test_shot:
        print("🧠 Connecting to Brain...")
        await brain.judge_image(test_shot) 
        print(f"✅ System Ready.")
        test_shot.close()
    else:
        print("❌ CRITICAL: Camera Failed. Check ADB Connection.")
    print("   (Monitoring started...)")
    print("-" * 50)

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

        wrong_app_detected = False
        if current_package:
            for ban_keyword in Config.BANNED_APPS_KEYWORDS:
                if ban_keyword.lower() in current_package.lower():
                    wrong_app_detected = True
                    print(f"\n🚨 BANNED APP DETECTED: {current_package}")
                    break

        just_punished = False

        if wrong_app_detected:
            strike_counter += 1
            print(f"⚠️ STRIKE {strike_counter}/{Config.MAX_STRIKES}")
            if strike_counter >= Config.MAX_STRIKES:
                await police.play_penalty_gif() 
                strike_counter = 0
            else:
                await police.soft_correction()
            just_punished = True
            
        elif not is_in_safe_zone and current_package != "" and "launcher" not in current_package:
             pass 

        # B. VISION CHECK
        if not just_punished and (time.time() - last_smart_check > Config.POLLING_RATE_SMART):
            print(".", end="", flush=True) 
            screenshot = await eyes.capture_screenshot()
            
            if screenshot:
                is_distracted = await brain.judge_image(screenshot)
                if is_distracted:
                    print("⛔ VISION VERDICT: DISTRACTION DETECTED.")
                    strike_counter += 1
                    print(f"⚠️ STRIKE {strike_counter}/{Config.MAX_STRIKES}")
                    
                    if strike_counter >= Config.MAX_STRIKES:
                        await police.play_penalty_gif()
                        strike_counter = 0
                    else:
                        await police.force_reset()
                    
                    just_punished = True
                screenshot.close()
            last_smart_check = time.time()

        if just_punished:
            print("\n🛡️  GRACE PERIOD: 8 seconds...")
            await asyncio.sleep(8)
            print("👀 Resuming watch.\n")
            continue

        await asyncio.sleep(Config.POLLING_RATE_FAST)

if __name__ == "__main__":
    asyncio.run(main())