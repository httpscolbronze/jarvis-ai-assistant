from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import asyncio
import os
from pathlib import Path
import shlex
import shutil
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
env_vars = dotenv_values(PROJECT_DIR / ".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
Username = env_vars.get("Username") or "JARVIS"

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
"LWkFKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]
messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {Username}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenTextFile(file_path):
        if os.name == "nt":
            subprocess.Popen(["notepad.exe", str(file_path)])
        else:
            subprocess.Popen(["xdg-open", str(file_path)])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": f"{Answer}"})
        return Answer
    
    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    file_path = PROJECT_DIR / "Data" / f"{Topic.lower().replace(' ', '')}.txt"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenTextFile(file_path)
    return True

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app):
    web_apps = {
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "x": "https://x.com",
        "gmail": "https://mail.google.com",
        "youtube": "https://youtube.com",
        "github": "https://github.com",
        "reddit": "https://reddit.com",
        "linkedin": "https://linkedin.com",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "https://open.spotify.com",
        "netflix": "https://netflix.com",
        "amazon": "https://amazon.com",
        "google": "https://google.com",
        "yahoo": "https://yahoo.com",
        "stackoverflow": "https://stackoverflow.com",
        "wikipedia": "https://wikipedia.org",
        "news": "https://news.google.com",
        "maps": "https://maps.google.com",
    }

    app = app.lower().strip()

    # Check if it is a known web application.
    if app in web_apps:
        webopen(web_apps[app])
        return True

    if os.name == "nt":
        try:
            from AppOpener import open as appopen
            appopen(app, match_closest=True, output=True, throw_error=True)
            return True
        except Exception as error:
            print(f"Local application not found: {error}")
    else:
        app_candidates = {
            "chrome": ("google-chrome", "chromium", "chromium-browser"),
            "google chrome": ("google-chrome", "chromium", "chromium-browser"),
            "files": ("thunar", "dolphin", "nautilus"),
        }.get(app, (app,))
        for candidate in app_candidates:
            executable = shutil.which(candidate)
            if executable:
                subprocess.Popen([executable])
                return True

        command = shlex.split(app)
        if command and shutil.which(command[0]):
            subprocess.Popen(command)
            return True

    website_url = f"https://{app.replace(' ', '')}.com"
    webopen(website_url)
    return True
    
def CloseApp(app):
    if os.name == "nt":
        try:
            from AppOpener import close
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except Exception:
            return False

    process_name = app.strip().split()[0] if app.strip() else ""
    if not process_name or not shutil.which("pkill"):
        return False
    return subprocess.run(
        ["pkill", "-x", process_name],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0

def System(command):
    if os.name == "nt":
        import keyboard
        key = {
            "mute": "volume mute",
            "unmute": "volume mute",
            "volume up": "volume up",
            "volume down": "volume down",
        }.get(command)
        if not key:
            return False
        keyboard.press_and_release(key)
        return True

    if shutil.which("wpctl"):
        actions = {
            "mute": ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "1"],
            "unmute": ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "0"],
            "volume up": ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"],
            "volume down": ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"],
        }
    elif shutil.which("pactl"):
        actions = {
            "mute": ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"],
            "unmute": ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"],
            "volume up": ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"],
            "volume down": ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"],
        }
    else:
        return False

    action = actions.get(command)
    return bool(action and subprocess.run(action, check=False).returncode == 0)

async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        
        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):  
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No Function found for {command}")

    results = await asyncio.gather(*funcs)

    for result in results: 
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
