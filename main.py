import asyncio
import time
import logging

# Suppress library logs
logging.getLogger("droidrun").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

from droidrun import DroidAgent, DroidrunConfig, AgentConfig, DeviceConfig
from modules.config import Config
from modules.eyes import ScreenEyes
from modules.brain import AcademicBrain
from modules.enforcer import PoliceOfficer
from modules.resource_manager import ResourceManager

async def main():
    print(f"--- 🛡️ Focus-Flow Pro ---")
    
    droid_config = DroidrunConfig(
        agent=AgentConfig(max_steps=10000), 
        device=DeviceConfig(platform="android")
    )
    base_agent = DroidAgent(goal="System", config=droid_config, llms={})

    resources = ResourceManager()
    eyes = ScreenEyes(base_agent)
    brain = AcademicBrain()
    police = PoliceOfficer(base_agent, resources)

    print("\n" + "="*40)
    print("🚦 SYSTEM ACTIVE: Safe Zone Enabled")
    print("   (Passive Mode - No Poking)")
    print("="*40)
    
    strike_counter = 0
    last_smart_check = 0
    
    while True:
        # A. SCAN
        screen_text = await eyes.scan()
        current_component = eyes.get_current_app_component()
        current_package = current_component.split('/')[0] if current_component else ""

        # --- SAFE ZONE LOGIC ---
        is_in_safe_zone = False
        if current_package:
            for safe_app in Config.SAFE_PACKAGES:
                if safe_app in current_package:
                    is_in_safe_zone = True
                    break

        wrong_app_detected = eyes.detects_distraction(screen_text, Config.BANNED_APPS_KEYWORDS)
        just_punished = False

        # 1. HARD CORRECTION (Not in Safe Zone)
        # Only punish if OUTSIDE safe zone AND NOT on launcher/home
        if not is_in_safe_zone and current_package != "" and "launcher" not in current_package:
            print(f"🚨 LEFT SAFE ZONE -> {current_package}")
            strike_counter += 1
            if strike_counter >= Config.MAX_STRIKES:
                await police.play_penalty_gif()
                strike_counter = 0
            else:
                await police.hard_correction()
            just_punished = True
        
        # 2. SPECIFIC BANNED APP (Double Check)
        elif wrong_app_detected:
            print(f"🚨 BANNED APP DETECTED -> {wrong_app_detected}")
            strike_counter += 1
            if strike_counter >= Config.MAX_STRIKES:
                await police.play_penalty_gif()
                strike_counter = 0
            else:
                await police.hard_correction()
            just_punished = True

        # 3. INSIDE SAFE ZONE (Content Check)
        elif is_in_safe_zone:
            # A. In-App Keywords (Shorts, Reels)
            in_app_distraction = eyes.detects_distraction(screen_text, Config.IN_APP_TRIGGERS)
            if in_app_distraction:
                print(f"🚨 IN-APP DISTRACTION -> {in_app_distraction}")
                strike_counter += 1
                if strike_counter >= Config.MAX_STRIKES:
                    await police.play_penalty_gif()
                    strike_counter = 0
                else:
                    await police.soft_correction()
                just_punished = True

            # B. Smart Check (AI Verification)
            elif time.time() - last_smart_check > Config.POLLING_RATE_SMART:
                print("🧠 AI Analyzing...")
                # We simply send the text. No poking.
                is_distracted = await brain.judge_content(screen_text)
                
                if is_distracted:
                    print("⚠️ Suspicious... Verifying (Double Check)...")
                    # Wait 2 seconds and check again to be sure (no poke, just passive scan)
                    await asyncio.sleep(2)
                    new_text = await eyes.scan()
                    
                    is_really_distracted = await brain.judge_content(new_text)
                    
                    if is_really_distracted:
                        print("⛔ DOUBLE VERIFIED: Irrelevant Content.")
                        strike_counter += 1
                        await police.force_reset()
                        just_punished = True
                    else:
                        print("✅ False Alarm (Second scan cleared).")
                else:
                    print("✅ VERDICT: Productive.")
                
                last_smart_check = time.time()

        # --- GRACE PERIOD ---
        if just_punished:
            print("\n🛡️  GRACE PERIOD: 5 seconds to return to work...")
            for i in range(5, 0, -1):
                print(f"   Scanning in {i}...", end="\r")
                await asyncio.sleep(1)
            print("\n👀 I am watching again.\n")
            continue

        await asyncio.sleep(Config.POLLING_RATE_FAST)

if __name__ == "__main__":
    asyncio.run(main())