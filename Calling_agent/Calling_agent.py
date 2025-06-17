# call_center_ai.py
import speech_recognition as sr
import pyttsx3
import openai
from openai import OpenAI

openai.api_key = 'key here'

client = OpenAI(
    api_key=openai.api_key,
)

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text):
    tts.say(text)
    tts.runAndWait()

def get_user_query():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Service is down."

def get_ai_response(query):
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": "You are a helpful call center assistant."},
                {"role": "user", "content": query}]
    )
    return response.choices[0].message.content.strip()

# Main loop
def start_call_center_ai():
    speak("Hello! How can I assist you today?")
    while True:
        query = get_user_query()
        print("User:", query)
        if "exit" in query.lower():
            speak("Thank you for calling. Have a great day!")
            break
        response = get_ai_response(query)
        print("AI:", response)
        speak(response)

if __name__ == "__main__":
    start_call_center_ai()
