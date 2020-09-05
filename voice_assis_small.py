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
        command=r.recognize_google(audio, language='en-in').lower()
        sofiaResponse('You said: ' +command+ '...hold on a sec.\n')
#loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Say that again please')
        command=myCommand();
    return command


def assistant(command):
    #making commands for the assistant, Sofia, to recognize
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







sofiaResponse('Robo Bobo Test')

#loop to continue the commands
while True:
    assistant(myCommand())