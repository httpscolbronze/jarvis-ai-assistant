
import os
from pathlib import Path

import cohere
from rich import print
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

# Model.py is inside Backend, so its parent directory is
# the actual JARVIS application root.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

# Load environment variables using the absolute path.
load_dotenv(dotenv_path=ENV_PATH)

# Retrieve Cohere API key.
CohereAPIKey = os.getenv("CohereAPIKey")

if not CohereAPIKey:
    raise ValueError(
        f"CohereAPIKey not found. Check your .env file at: {ENV_PATH}"
    )

# Initialize Cohere V2 client.
co = cohere.ClientV2(api_key=CohereAPIKey)

print("[green]Cohere client initialized successfully![/green]")


# ============================================================
# FUNCTION KEYWORDS
# ============================================================

funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder", "send message",
    "whatsapp to", "telegram to"
]


# ============================================================
# MESSAGE STORAGE
# ============================================================

messages = []


# ============================================================
# DECISION-MAKING MODEL PROMPT
# ============================================================

preamble = """
You are a very accurate Decision-Making Model, which decides what kind
of a query is given to you.

You will decide whether a query is a 'general' query, a 'realtime'
query, or is asking to perform any task or automation.

*** Do not answer any query, just decide what kind of query is given
to you. ***

-> Respond with 'general (query)' if a query can be answered by an
LLM model and doesn't require up-to-date information.

-> Respond with 'realtime (query)' if a query requires up-to-date
information, such as current news or recent updates.

-> Respond with 'open (application name or website name)' if a query
is asking to open an application or website.

-> Respond with 'close (application name)' if a query is asking
to close an application.

-> Respond with 'play (song name)' if a query is asking to play music.

-> Respond with 'generate image (image prompt)' if a query is
requesting image generation.

-> Respond with 'reminder (datetime with message)' if a query is
requesting a reminder.

-> Respond with 'system (task name)' if a query is asking to control
system functions such as volume or mute.

-> Respond with 'content (topic)' if a query is asking to write
content, applications, code, emails, etc.

-> Respond with 'send message (contact name message)' if a query
is asking to send a normal message.

-> Respond with 'whatsapp to (contact name message)' if a query
is asking to send a WhatsApp message.

-> Respond with 'telegram to (contact name message)' if a query
is asking to send a Telegram message.

-> Respond with 'google search (topic)' if a query is asking
to search Google.

-> Respond with 'youtube search (topic)' if a query is asking
to search YouTube.

*** If the query asks to perform multiple tasks, return each
task separately, separated by commas. ***

*** If the user says goodbye or wants to end the conversation,
respond with 'exit'. ***

*** Respond with 'general (query)' if you cannot decide the
kind of query or if the requested task is not listed. ***

IMPORTANT:
Only return task classifications.
Do not provide explanations or additional text.
"""


# ============================================================
# CHAT HISTORY
# ============================================================

ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},

    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},

    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {
        "role": "Chatbot",
        "message": "open chrome, general tell me about mahatma gandhi."
    },

    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},

    {
        "role": "User",
        "message": "what is today's date and remind me about my performance"
    },
    {
        "role": "Chatbot",
        "message": "general what is today's date, reminder performance"
    },

    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."},

    {
        "role": "User",
        "message": "send a message to mom that i will be late today."
    },
    {
        "role": "Chatbot",
        "message": "send message mom i will be late today."
    },

    {
        "role": "User",
        "message": "whatsapp to dad that i will be there in 5 minutes."
    },
    {
        "role": "Chatbot",
        "message": "whatsapp to dad i will be there in 5 minutes."
    },

    {
        "role": "User",
        "message": "telegram to brother i will be late today."
    },
    {
        "role": "Chatbot",
        "message": "telegram to brother i will be late today."
    }
]


# ============================================================
# FIRST LAYER DECISION-MAKING MODEL
# ============================================================

def FirstLayerDMM(prompt: str = "test"):

    messages.append({
        "role": "user",
        "content": prompt
    })

    # Create Cohere streaming response.
    stream = co.chat_stream(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "system",
                "content": preamble
            },
            *[
                {
                    "role": (
                        "user"
                        if item["role"] == "User"
                        else "assistant"
                    ),
                    "content": item["message"]
                }
                for item in ChatHistory
            ],
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    # Collect generated response.
    response = ""

    for event in stream:

        if event.type == "content-delta":

            text = event.delta.message.content.text

            if text:
                response += text

    # Process response.
    response = response.replace("\n", "")

    response = [
        task.strip()
        for task in response.split(",")
    ]

    # Filter recognized functions.
    temp = []

    for task in response:

        for func in funcs:

            if task.startswith(func):
                temp.append(task)
                break

    response = temp

    # Retry if the model returns an incomplete query.
    if "(query)" in response:
        return FirstLayerDMM(prompt=prompt)

    return response


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":

    print("[bold cyan]JARVIS Decision-Making Model[/bold cyan]")

    while True:

        try:
            user_input = input(">>> ")

            if user_input.lower().strip() in [
                "exit",
                "quit",
                "shutdown"
            ]:
                break

            result = FirstLayerDMM(user_input)

            print(result)

        except KeyboardInterrupt:
            print("\n[yellow]JARVIS Model stopped.[/yellow]")
            break

        except Exception as e:
            print(f"[red]Error: {e}[/red]")
