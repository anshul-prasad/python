import speech_recognition as sr
import os
from gtts import gTTS
import tempfile
import openai
import webbrowser
import subprocess
import datetime
import time
from config import API_URL, GH_API_TOKEN
client = openai.OpenAI(base_url=API_URL, api_key=GH_API_TOKEN, timeout=60)

chatStr = ""


def chat(query):
    global chatStr

    chatStr += f"\nAnshul: {query}\nJarvis: "
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are Jarvis AI."},
            {"role": "user", "content": f"{chatStr}"},
        ],
    )
    chatStr += f"{response.choices[0].message.content}"
    # print(chatStr)
    say(response.choices[0].message.content)
    return response.choices[0].message.content


def ai(query):
    text = f"OpenAI response for prompt: {query}\n*********************************\n\n"
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are Jarvis."},
            {"role": "user", "content": f"{query}"},
        ],
    )
    text += response.choices[0].message.content

    if not os.path.exists("openai"):
        os.mkdir("openai")

    if len(" ".join(query.strip().split("intelligence")[1:])) >= 30:
        file_name = f"openai/{' '.join(query.strip().split('intelligence')[1:])}.txt"
    else:
        file_name = f"openai/{' '.join(query.strip().split('intelligence')[1:])}.txt"

    with open(file_name, "w") as f:
        f.write(text)


def say(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name
    tts.save(filename)
    os.system(
        f"mpg123 {filename} > /dev/null 2>&1"
    )  # run command in terminal and stop terminal logs
    os.remove(filename)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone(device_index=5) as source:
        r.energy_threshold = 300
        r.pause_threshold = 1
        print("\nListening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            time.sleep(2)
            return query
        except sr.UnknownValueError:
            print("could not understand")
            return ""
        except sr.RequestError as e:
            print("API error:", e)
            return ""


if __name__ == "__main__":
    say("Jarvis A.I.")
    while True:
        print("Ask question.")
        query = take_command()

        if "jarvis quit" in query.lower():
            exit()

        elif "open" in query:
            # open site
            sites = [
                ["youtube", "https://www.youtube.com"],
                ["wikipedia", "https://www.wikipedia.com"],
                ["google", "https://www.google.com"],
            ]
            for site in sites:
                if f"open {site[0]}" in query.lower():
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])

        # play music
        elif f"play music" in query.lower():
            subprocess.run(
                [
                    "xdg-open",
                    "Major Lazer - Cold Water (feat. Justin Bieber & MØ) [Official Dance Video].mp3",
                ]
            )

        # tell time
        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strfTime}")

        # open terminal in ubuntu (linux)
        elif "open terminal" in query:
            say(f"Sir Terminal is opening...")
            subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c", "ls -la; exec bash"]
            )

        # For answers to a query
        elif "artificial intelligence" in query.lower():
            ai(query)

        # For chatting
        else:
            print("Chatting...")
            chat(query)

        # weather
        # news
        # many more functionalities can be added
