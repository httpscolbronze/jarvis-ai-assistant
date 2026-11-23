import speech_recognition as sr
from dotenv import dotenv_values
from pathlib import Path
import mtranslate as mt

PROJECT_DIR = Path(__file__).resolve().parents[1]
env_vars = dotenv_values(PROJECT_DIR / ".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")
TempDirPath = PROJECT_DIR / "Frontend" / "Files"
TempDirPath.mkdir(parents=True, exist_ok=True)
recognizer = sr.Recognizer()

# Function to set the assistant's status by writing it to a file.
def SetAssistantStatus(Status):
    with (TempDirPath / "Status.data").open("w", encoding="utf-8") as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    if not query_words:
        return ""
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "wh"]

    # Check if the query is a question and add a question mark if necessary.
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '?'
        else:
            new_query += '?'
    else:
        # Add a period if the query is not a question.
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '.'
        else:
            new_query += '.'
    return new_query

# Function to translate text into English using the mtranslate library.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to capture and transcribe speech from the default microphone.
def SpeechRecognition():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        return recognizer.recognize_google(audio, language=InputLanguage)
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as error:
        print(f"Speech recognition service unavailable: {error}")
        return ""

# Main execution block.
if __name__ == "__main__":
    while True:
        try:
            Text = SpeechRecognition()
            if InputLanguage.lower().startswith("en"):
                print(QueryModifier(Text))
            else:
                SetAssistantStatus('Translating ...')
                print(QueryModifier(UniversalTranslator(Text)))
        except Exception as e:
            print(f"An error occurred: {e}")
            break