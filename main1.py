import streamlit as st
import datetime
import os
#from ecapture import ec
import wikipedia
import json
from urllib.request import urlopen
import webbrowser
import pyjokes
import pyttsx3
import smtplib
import time
import requests
import openai
import speech_recognition as sr
import winshell
import subprocess
from config import apikey, password

openai.api_key = apikey

def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning!"

    elif 12 <= hour < 18:
        return "Good Afternoon!"

    else:
        return "Good Evening!"

def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('vishnukv2349@ieee.org', password)
    server.sendmail('your email id', to, content)
    server.close()

def ai(prompt):
    messages = [{"role": "system", "content": "You are an intelligent assistant."}]
    message = prompt
    if message:
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        return reply



def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("recognizing..")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Some Error Occurred, Please say the Commands again")

def main():
    print("say")
    st.title("AVA - Your Virtual Assistant")
    st.sidebar.write("Voice Assistant")

    if st.sidebar.button("Start AVA"):
        st.write("Hello, I am AVA")
        st.write(wishme())
        #st.write("What should I call you?")
        #uname = st.text_input("Your Name")
        st.write(f"Welcome")
        st.write("How can I help you?")

        while True:
            st.write("Listening...")
            query = take_command()
            st.write(take_command())
            sites = [["youtube", "https://youtube.com"], ["instagram", "https://instagram.com"],
                     ["google", "https://google.com"]]
            if query:
                for site in sites:
                    if f"open {site[0]}".lower() in query:
                        st.write(f"Opening {site[0]}")
                        say(f"Opening {site[0]}")
                        webbrowser.open(site[1])

                if "the time" in query:
                    st.write(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")
                    say(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")
                elif 'how are you' in query:
                    st.write("I am fine, Thank you. How are you?")
                    say("I am fine, Thank you. How are you?")
                elif 'joke' in query:
                    st.write(pyjokes.get_joke())
                    say(pyjokes.get_joke())
                elif 'wikipedia' in query.lower():
                    st.write('Searching Wikipedia...')
                    say('Searching Wikipedia...')
                    try:
                        query = query.replace("wikipedia", "")
                        results = wikipedia.summary(query, sentences=3)
                        st.write(results)
                        say(results)
                    except Exception as e:
                        st.write("Sorry, I am not able to find anything")
                        say("Sorry, I am not able to find anything")
                elif 'send a mail' in query:
                    try:
                        st.write("What should I say?")
                        say("What should I say?")
                        content = take_command()
                        st.write("whom should i send?")
                        say("whom should i send?")
                        to = input()
                        send_email(to, content)
                        st.write("Email has been sent!")
                        say("Email has been sent!")
                    except Exception as e:
                        st.write("I am not able to send this email")
                        say("I am not able to send this email")
                elif "don't listen" in query or "stop listening" in query:
                    st.write("For how much time you want to stop AVA from listening to commands?")
                    say("For how much time you want to stop AVA from listening to commands?")
                    time.sleep(int(take_command()))
                elif 'open brave' in query:
                    codePath = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk"
                    os.startfile(codePath)
                elif 'news' in query:
                    try:
                        jsonObj = urlopen(
                            '''https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=81025fc3636f4097ad33b6dc5f87d87c''')
                        data = json.load(jsonObj)
                        i = 1

                        st.write('Here are some top news from the Times of India')
                        for item in data['articles']:
                            st.write(f"{i}. {item['title']}")
                            say(f"{i}. {item['title']}")
                            st.write(item['description'])
                            say(item['description'])
                            i += 1

                    except Exception as e:
                        st.write(str(e))
                elif 'exit' in query:
                    st.write("Thanks for giving me your time")
                    say("Thanks for giving me your time")
                    break
                else:
                    st.write("Chatting...")
                    reply = ai(query)
                    st.write(reply)
                    say(reply)
def say(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 70)
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    main()