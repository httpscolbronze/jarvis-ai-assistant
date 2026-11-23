# JARVIS - AI Virtual Assistant

An advanced AI-powered virtual assistant desktop application built with Python, PyQt5, Groq, Cohere, and Hugging Face.

> **⚠️ Platform Notice:** JARVIS is exclusively designed and built to work on **Microsoft Windows**. Certain core automation libraries (`AppOpener`, Windows-specific automation hooks, etc.) and desktop integrations are natively tailored for Windows environments.

---

## Features

- **Voice & Chat Interface:** Interactive PyQt5 graphical user interface with real-time speech recognition and text-to-speech feedback (Edge-TTS).
- **AI Models:** Integrates Groq, Cohere, and Hugging Face models for intelligent conversation and task handling.
- **Automation & Tools:** Web searching, automated app launching, system controls, and media playback.
- **Vision Integration:** Image analysis and generation capabilities.

---

## Prerequisites (Windows)

- **Python 3.10+** installed and added to PATH.
- **PortAudio** (required for PyAudio / SpeechRecognition).

---

## Installation & Setup

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/YOUR_USERNAME/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. **Create and activate a virtual environment:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   python -m pip install --upgrade pip
   python -m pip install -r Requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and fill in your API keys (Groq, Cohere, Hugging Face, Tavily, etc.):
   ```cmd
   copy .env.example .env
   ```

5. **Run the Application:**
   ```cmd
   python main.py
   ```

---

## Requirements

Listed in [Requirements.txt](Requirements.txt), including:
- PyQt5
- Groq / Cohere / Hugging Face Hub
- SpeechRecognition & PyAudio
- Edge-TTS
- Pillow, Rich, Requests, Pygame, etc.

---

## License

This project is licensed under the MIT License.
