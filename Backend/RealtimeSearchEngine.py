from tavily import TavilyClient
from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.
from pathlib import Path

# Load environment variables from the .env file.
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "Data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHAT_LOG_PATH = DATA_DIR / "ChatLog.json"
env_vars = dotenv_values(PROJECT_DIR / ".env")

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
TavilyAPIKey = env_vars.get("TavilyAPIKey")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)
tavily_client = TavilyClient(api_key=TavilyAPIKey)

# Define the system instructions for the chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with CHAT_LOG_PATH.open("r", encoding="utf-8") as f:
        messages = load(f)
except:
    with CHAT_LOG_PATH.open("w", encoding="utf-8") as f:
        dump([], f)

# Function to perform a Tavily search and format the results.
def TavilySearch(query):
    try:
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=3
        )

        Answer = f"The search results for '{query}' are:\n[start]\n"

        for result in response["results"]:
            Answer += f"Title: {result['title']}\n"
            Answer += f"URL: {result['url']}\n"
            Answer += f"Content: {result['content'][:1200]}\n\n"

        Answer += "[end]"
        return Answer

    except Exception as e:
        return f"[Tavily search failed: {e}]"

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time.
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"""
    Use This Real-time Information if needed:
    Day: {day}
    Date: {date}
    Month: {month}
    Year: {year}
    Time: {hour} hours, {minute} minutes, {second} seconds.
    """
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load the chat log from the JSON file.
    with CHAT_LOG_PATH.open("r", encoding="utf-8") as f:
        messages = load(f)

    messages.append({"role": "user", "content": prompt})

    # Add Tavily search results to the system chatbot messages.
    SearchResults = TavilySearch(prompt)
    SystemChatBot.append({"role": "system", "content": SearchResults})

    try:
        # Generate a response using the Groq Client.
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        # Concatenate response chunks from the streaming output.
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        # Clean up the response.
        Answer = Answer.strip().replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log back to the JSON file.
        with CHAT_LOG_PATH.open("w", encoding="utf-8") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"RealtimeSearchEngine Error: {e}")
        return "Sorry, I was unable to retrieve or process the real-time information right now."

    finally:
        # Always remove the temporary Tavily system message.
        SystemChatBot.pop()


# Main entry point of the program for interactive querying.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))