from flask import Flask, render_template, jsonify
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

app = Flask(__name__)

# Jarvis Initialization
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your Key Here>"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key="your_screat_key")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        return "Opened Google."
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        return "Opened Facebook."
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        return "Opened YouTube."
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        return "Opened LinkedIn."
    elif "open instagram" in c.lower():
        webbrowser.open("www.instagram.com")
        return "Opened instagram."
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
            return f"Playing {song}."
        return "Song not found."
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            headlines = [article['title'] for article in articles[:5]]  # Fetch top 5 headlines
            return " ".join(headlines)
        else:
            return "Unable to fetch news."
    else:
        output = aiProcess(c)
        return output

@app.route("/")
def index():
    return render_template("jarvis.html")

@app.route("/process_voice", methods=["POST"])
def process_voice():
    try:
        # Listen to the user's voice command
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        response = processCommand(command)

        # Speak and return the response
        speak(response)
        return jsonify({"response": response})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        speak(error_message)  # Speak the error as well
        return jsonify({"response": error_message})

if __name__ == "__main__":
    app.run(debug=True)
