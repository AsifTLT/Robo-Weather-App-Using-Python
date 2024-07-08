import requests
import pyttsx3
import json
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# The assistant introduces itself and asks for the city name
engine.say("Hi, I am your virtual assistant. Tell me the name of the place whose temperature and weather you want to know.")
engine.runAndWait()

# Initialize the recognizer
recognizer = sr.Recognizer()

# Capture audio input from the user
with sr.Microphone() as source:
    print("Listening for the city name...")
    audio = recognizer.listen(source)

# Recognize the speech input
try:
    city = recognizer.recognize_google(audio)
    print(f"You said: {city}")

    # Formatting the URL with the city name
    url = f"https://api.weatherapi.com/v1/current.json?key=2a54e03ee9ce483281c51930240807&q={city}"

    # Making the API request
    r = requests.get(url)
    wdic = json.loads(r.text)

    # Extracting temperature and weather condition
    w = wdic["current"]["temp_c"]
    c = wdic["current"]["condition"]["text"]

    # The assistant provides the temperature and weather condition
    engine.say(f"The current temperature in {city} is {w} degrees Celsius and the weather is {c}.")
    engine.runAndWait()

except sr.UnknownValueError:
    engine.say("Sorry, I could not understand the city name. Please try again.")
    engine.runAndWait()

except sr.RequestError as e:
    engine.say("Could not request results; {0}".format(e))
    engine.runAndWait()

except KeyError:
    engine.say("Sorry, I couldn't find the weather information for the city you mentioned.")
    engine.runAndWait()
