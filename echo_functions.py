import speech_recognition as sr
from dotenv import load_dotenv
import requests
import pyttsx3
import os
from simple_colors import *
import operator
import time
import sys

def listen():
    text = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk")
        audio = r.listen(source)
    flag = False

    try:
        text = r.recognize_google(audio, language="eng")
        text.replace("estanbul", "Istanbul")
        print(text)
        flag = True
    except sr.UnknownValueError:
        print(red("[X]") + "Please Talk Again")

    except sr.RequestError as e:
        print(red("[X]") + "Internet Error; {0}".format(e))

    return flag,text

def check(text, key):
    def classify(text):
        url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"

        response = requests.get(url, params={"data": text})

        if response.ok:
            responseData = response.json()
            topMatch = responseData[0]
            return topMatch
        else:
            response.raise_for_status()
    demo = classify(text)
    label = demo["class_name"]
    confidence = demo["confidence"]
    return label,confidence

def answer(label,confidence,flag, voice_id):
    if flag == True:
        if confidence > 65 and label == "how_are_you":
            answer_w_speech = "I am fine thanks, how about you?"
        elif confidence > 65 and label == "answer_how_are_you":
            answer_w_speech = "Cool"
        elif confidence > 65 and label == "answer_how_are_you_negative":
            answer_w_speech = "I hope you'll be fine"
        elif confidence > 65 and label == "hi":
            answer_w_speech = "Hi, how are you?"
        elif confidence > 65 and label == "made_in":
            answer_w_speech = "I was designed by Adnan in Turkey."
        elif confidence > 65 and label == "thank_you":
            answer_w_speech = "No worries."
        elif confidence > 65 and label == "clear_screen":
            answer_w_speech = "Clearing Screen..."
            os.system('cls')
        elif confidence > 65 and label == "change_voice":
            change_voice_text = "Which voice do you want to select" + "\n" "[1] Male" + "\n" "[2] Female"
            print(change_voice_text)
            say(change_voice_text, voice_id)
            answer_w_speech = ""
            voice_change()
        elif confidence > 65 and label == "math":
            print("Say what you want to calculate, example: 3 plus 3")
            flag, text_math = listen()
            answer_w_speech = (eval_binary_expr(*(text_math.split())))
        elif confidence > 65 and label == "time_hour":
            current_time = get_time()
            answer_w_speech = "It's " + current_time
        elif confidence > 65 and label == "weather":
            get_weather()
            answer_w_speech = ""
        elif confidence > 65 and label == "exit_assistant":
            answer_w_speech = "Good bye."
            print(answer_w_speech)
            say(answer_w_speech, voice_id)
            sys.exit()
        else:
            answer_w_speech = "I think I couldn't understand, can you say it again."
        print(answer_w_speech)
        say(answer_w_speech, voice_id)

def voice_change():
    flag, text = listen()
    label, confidence = check(text)

    if confidence > 65 and label == "sex_male":
        answer_w_speech = yellow("[!]") + "Voice changed to male"
        with open('voice_id.txt', "w") as myfile:
            myfile.write("0")
            myfile.close()
    elif confidence > 65 and label == "sex_female":
        answer_w_speech = yellow("[!]") + "Voice changed to female"
        with open('voice_id.txt', "w") as myfile:
            myfile.write("1")
            myfile.close()
    else:
        answer_w_speech = red("[X]") + "Can you say it again."
        voice_change()
    with open('voice_id.txt', "r") as myfile:
        voice_id = int(myfile.read())
    print(answer_w_speech)
    say(answer_w_speech, voice_id)
    exec(open("Echo Assistant.py").read())
    return voice_id


def say(answer_w_speech, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.say(answer_w_speech)
    engine.runAndWait()

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        'divided' :operator.__truediv__,
        'Mod' : operator.mod,
        'mod' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, oper, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(oper)(op1, op2)

def get_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    return current_time

def get_weather():
    api_key = os.getenv("api_key")
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    print("City name : ")
    flag, text = listen()
    city_name = text
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature = round(current_temperature) - 273
        z = x["weather"]
        weather_description = z[0]["description"]
        print(" Temperature (in celcius) = " + str(current_temperature) + "\n description = " + str(weather_description))
    else:
        print("City Not Found")