import pyttsx3
import webbrowser
import speech_recognition as sr
import musicLib
import pyautogui
import requests

# Initialize the TTS engine
engine = pyttsx3.init()
NEWS_API_KEY = "ab0d7d1cd395419ba1723d2c20e86805"

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_news(category=None):
    speak("Fetching the latest news. Please wait.")

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "apiKey": NEWS_API_KEY,
        "country": "us",
        "pageSize": 5,
    }

    if category:
        params["category"] = category

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200 or data.get("status") != "ok":
            print("News API error:", data.get("message", "Unknown error"))
            speak("Sorry, I could not fetch the news.")
            return

        articles = data.get("articles", [])

        if not articles:
            speak("Sorry, no news articles were found.")
            return

        speak("Here are the latest headlines.")

        for i, article in enumerate(articles, start=1):
            title = article.get("title")
            print(f"News {i}. {title}")
            speak(f"News {i}. {title}")
    
    except Exception as e:
         print(f"Error: {e}")

def speech(c):
    print(c)

    if "open google" in c.lower():
        speak("Open Google")
        print("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        speak("Open Youtube")
        print("Opening Youtube")
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in c.lower():
        speak("Open Linkedin")
        print("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com")
    elif "play" in c.lower():
        d = c.lower().split("play",1)[1].strip()
        b = musicLib.music[d]
        webbrowser.open(b)
    elif "pause" in c.lower() or "continue" in c.lower():
        pyautogui.press("k")

    elif "news" in c.lower():
        if "technology" in c.lower() or "tech" in c.lower():
           return get_news("technology")

        elif "sports" in c.lower():
           return get_news("sports")

        elif "business" in c.lower():
            return get_news("business")

        elif "science" in c.lower():
           return get_news("science")

        elif "entertainment" in c.lower():
           return get_news("entertainment")
        else:
             return get_news()
        # # Exit condition
    elif "exit" in c or "quit" in c:
        speak("Goodbye!")
        break


# Main loop
while True:
    recognizer = sr.Recognizer()
    speak("Initializing Jarvis... Listening now.")
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
        # Convert speech to text
        word = recognizer.recognize_google(audio)
        print(word)

        #  Activate Jarvis on keyword
        if word.lower() == "jarvis":
            speak("Yes boss, How i assist you")
            print("Jarvis Active")

        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=4)
        # Convert speech to text
        command = recognizer.recognize_google(audio)
        
        speech(command)
        
    except Exception as e:
        print(f"Error: {e}")
