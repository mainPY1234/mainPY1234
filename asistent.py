import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from time import ctime, sleep
import datetime

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize reminders list
reminders = []

# Initialize jokes list
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "What do you get when you cross a snowman and a vampire? Frostbite."
]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def record_audio(ask=False, timeout=5):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
        audio = r.listen(source, timeout=timeout)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that")
        except sr.RequestError as e:
            speak("Sorry, my speech service is down")
        return voice_data

def add_reminder(reminder, time):
    reminders.append({"reminder": reminder, "time": time})

def check_reminders():
    current_time = datetime.datetime.now().strftime("%H:%M")
    for reminder in reminders:
        if reminder["time"] == current_time:
            speak(f"Reminder: {reminder['reminder']}")
            reminders.remove(reminder)

def open_application(app_name):
    if app_name == "notepad":
        os.system("notepad")
    elif app_name == "calculator":
        os.system("calc")
    elif app_name == "google":
        webbrowser.get().open("https://www.google.com")
    else:
        speak("Application not available")

def control_volume(action):
    if action == "increase":
        os.system("nircmd.exe changesysvolume 2000")  # Increase volume
    elif action == "decrease":
        os.system("nircmd.exe changesysvolume -2000")  # Decrease volume
    elif action == "mute":
        os.system("nircmd.exe mutesysvolume 1")  # Mute volume
    elif action == "unmute":
        os.system("nircmd.exe mutesysvolume 0")  # Unmute volume
    else:
        speak("Volume control action not recognized")

def respond(voice_data):
    if 'what is your name' in voice_data:
        speak("My name is Alaxes")
    elif 'how old are you' in voice_data:
        speak("I am as old as time itself")
    elif 'time' in voice_data:
        speak(ctime())
    elif 'search' in voice_data:
        search = record_audio("What do you want to know?")
        url = 'http://google.com/search?q=' + search
        webbrowser.get().open(url)
        speak("Here is what I found for " + search)
    elif 'location' in voice_data:
        location = record_audio("What is the location?")
        url = 'http://google.nl/maps/place/' + location + '/&amp'
        webbrowser.get().open(url)
        speak("Here is the location of " + location)
    elif 'joke' in voice_data:
        joke = jokes.pop(0)
        jokes.append(joke)
        speak(joke)
    elif 'remind me' in voice_data:
        reminder = record_audio("What do you want to be reminded about?")
        time = record_audio("At what time? Please specify in HH:MM format.")
        add_reminder(reminder, time)
        speak(f"Reminder set for {time} to {reminder}")
    elif 'open' in voice_data:
        app_name = record_audio("Which application would you like to open?")
        open_application(app_name.lower())
    elif 'volume' in voice_data:
        action = record_audio("Would you like to increase, decrease, mute, or unmute the volume?")
        control_volume(action.lower())
    elif 'well done' in voice_data:
        speak("Thank you")
    elif 'exit' in voice_data:
        speak("Goodbye!")
        exit()  # Exit the program
    else:
        speak("Sorry, I don't know how to help with that")

# Initial prompt
speak("How can I assist you?")

# Continuous interaction loop
while True:
    try:
        voice_data = record_audio(timeout=5)  # Wait for 5 seconds for user response
        if voice_data:
            respond(voice_data)
            check_reminders()
    except sr.WaitTimeoutError:
        speak("I'm waiting for your command...")
    except KeyboardInterrupt:
        speak("Goodbye!")
        break  # Exit the program on keyboard interrupt (Ctrl+C)
