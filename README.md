
# 🛡️ FocusFlow Pro: AI-Powered Accountability Agent

**FocusFlow Pro** is an **Autonomous Android Agent** that visually monitors your productivity and enforces discipline through social accountability.

It uses **Computer Vision (Google Gemini 2.5 Flash)** to analyze your screen in real-time. If it detects you are distracted, it intervenes. If you persist, it takes control of your phone to report you to an accountability partner via WhatsApp.

---

## Powered by DroidRun

This project is built on the **DroidRun** framework, which transforms standard ADB commands into a structured Agentic workflow.

Instead of writing rigid scripts (e.g., "tap x,y"), FocusFlow uses DroidRun's `DroidAgent` architecture to create a cognitive loop:

1. **Observation:** The agent perceives the device state through the `ScreenEyes` module.
2. **Reasoning:** The `AcademicBrain` (LLM) interprets the visual context against the user's goal.
3. **Action:** The `PoliceOfficer` module executes high-level intents (like searching for a specific contact name) rather than blind coordinate taps.

DroidRun provides the essential "Body" that connects the "Brain" (Gemini) to the Android operating system, handling device state, logging, and tool execution reliability.

---

## Key Features

* **Vision-Based Intelligence:** Unlike standard blockers that just check package names, FocusFlow "sees" your screen. It can distinguish between a "Biology PDF" (Productive) and "Spiderman Gameplay" (Distracted) even if they are in the same app.
* **The Snitch Protocol:** If you reach **3 Strikes**, the Agent takes control of the WhatsApp UI, searches for your designated contact (e.g., "Dad"), and auto-sends a shame message reporting your distraction.
* **Stealth Monitoring:** Captures screenshots directly to RAM (no files saved) and resizes them for ultra-fast (<0.2s) AI analysis.
* **Escalating Enforcement:**
* **Strike 1-2:** Soft Correction (Back Button) + Browser Warning Popup.
* **Strike 3:** Plays an annoying penalty GIF & executes the Snitch Protocol.



---

## Prerequisites

* **Python 3.10+**
* **Android Device:** Connected via USB with **USB Debugging Enabled**.
* **ADB (Android Debug Bridge):** Must be installed and accessible in your system path.
* **Google Gemini API Key:** Get one for free at [Google AI Studio](https://aistudio.google.com/).

---

## Installation

1. **Clone the Repository**
```bash
git clone https://github.com/NotShura/focus-flow.git
cd FocusFlow

```


2. **Install Dependencies**
```bash
pip install google-generativeai droidrun pillow python-dotenv

```


3. **Project Structure Setup**
The agent requires a specific folder structure for the penalty assets.
* Create the folders: `assets/images/`
* Place an annoying GIF file named `penalty.gif` inside `assets/images/`.


**Final Layout:**
```text
FocusFlow/
├── main.py
├── .env                <-- Create this file
├── modules/
│   ├── brain.py
│   ├── config.py
│   ├── enforcer.py
│   └── eyes.py
└── assets/
    └── images/
        └── penalty.gif <-- REQUIRED

```


4. **Configure API Key**
Create a `.env` file in the root directory and add your key:
```env
GEMINI_API_KEY=your_actual_api_key_here

```



---

## Usage

1. **Connect your Phone**
Ensure your device appears when you run:
```bash
adb devices

```


2. **Run the Agent**
```bash
python main.py

```


3. **Follow the On-Screen Prompts**
* **Enter Accountability Contact:** e.g., `Dad` (Must match the *exact* name saved in your WhatsApp).


4. **Get to Work!**
The terminal will print a dot `.` for every scan.
* **Productive?** Silence.
* **Distracted?** The agent will warn you.
* **Strike 3?** The agent will open WhatsApp and snitch on you.



---

## Architecture

FocusFlow operates on a modular Agentic architecture:

* **Eyes (`eyes.py`):** Captures screen data via ADB pipe directly to memory (avoiding disk I/O). Optimizes images to 480px for high-speed upload.
* **Brain (`brain.py`):** Sends the visual data to Google Gemini 2.5 Flash. It uses a "Productivity Whitelist" logic—if the screen doesn't look like Study/Work, it is automatically flagged as a distraction.
* **Enforcer (`enforcer.py`):** The "Muscle." It executes ADB input events. It contains the logic for the **Agentic WhatsApp Search**, simulating human touches to find a contact and send a message.

---

## Disclaimer & Privacy

* **Privacy:** Screenshots are processed in **RAM only** and sent to Google's API for analysis. They are not saved to your local hard drive.
* **Use at your own risk:** This software automates user inputs (taps/swipes). While designed to be safe, the authors are not responsible for accidental messages sent or app interactions.

