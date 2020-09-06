import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime

#this method will convert text to speech
def sofiaResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system('say '+audio)
        
def myCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        sofiaResponse('Listening...')
        r.adjust_for_ambient_noise(source, duration=1)
        audio=r.listen(source, phrase_time_limit=5)
    try:
        command=r.recognize_google(audio).lower()
        sofiaResponse('You said: ' +command+ '...hold on a sec.\n')
#loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Say that again please')
        command=myCommand();
    return command




def assistant(command):
    #making commands for the assistant, Sofia, to recognize

    #opening a subreddit
    if 'open reddit' in command:
        reg_ex=re.search('open reddit (.*)', command)
        url='https://www.reddit.com/'
        if reg_ex:
            subreddit=reg_ex.group(1)
            url= url + 'r/' + subreddit
            sofiaResponse('searching')
        webbrowser.open(url)
        sofiaResponse('The Reddit content has been opened for you!')
    elif 'shutdown' in command:
        sofiaResponse('Goodbye from Reddit!')
        sys.exit()

    #opening a website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse('I\ve opened the website.')
        else:
            pass

    #greetings
    elif 'greetings' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello and Good morning')
        elif 12 <= day_time < 18:
            sofiaResponse('Hello and Good afternoon')
        else:
            sofiaResponse('Hello and Good evening')
    
    #assistant tells you its options
    elif 'help' in command:
        sofiaResponse('I am pulling up the options for you')
        sofiaResponse("""
        You can use these commands and I'll help you out:
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Tell a joke/another joke : Says a random dad joke.
        5. Current weather in {cityname} : Tells you the current condition and temperture
        7. Greetings
        8. play me a video : Plays song in your VLC media player
        9. change wallpaper : Change desktop wallpaper
        10. news for today : reads top news of today
        11. time : Current system time
        12. top stories from google news (RSS feeds)
        13. tell me about xyz : tells you about xyz
        """)
        pass

    #top stories from google news
    elif 'news' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                sofiaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)
       






sofiaResponse('Robo Bobo Test')

#loop to continue the commands
while True:
    assistant(myCommand())