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
#import vlc
#import urllib
#import urllib2
import urllib.request
import json
from bs4 import BeautifulSoup as soup
#from urllib2 import urlopen
from urllib.request import urlopen
import wikipedia
import random
from time import strftime

def myCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source, duration=1)
        audio=r.listen(source)
    try:
        command=r.recognize_google(audio).lower()
        print('You said: '+command+'\n')
#loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command=myCommand();
    return command
#this method will convert text to speech
def sofiaResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system('say '+audio)

def assistant(command):

#making commands for the assistant, Sofia, to recognize
    if 'open reddit' in command:
        reg_ex=re.search('open reddit (.*)', command)
        url='https://www.reddit.com/'
        if reg_ex:
            subreddit=reg_ex.group(1)
            url= url + 'r/' + subreddit
        webbrowser.open(url)
        sofiaResponse('The Reddit content has been opened for you!')
    elif 'shutdown' in command:
        sofiaResponse('Goodbye from Reddit!')
        sys.exit()
        
#more website opening commands!
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url= 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse('The website you have requested has been opened for you!')
        else:
            pass
#send an email
    elif 'email' in command:
        sofiaResponse('Who ßam I sending this to?')
        recipient= myCommand()
        if 'matt' in recipient:
            sofiaResponse('What should I say to them?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email_address', 'your_password')
            mail.sendmail('sender_email', 'receiver_email', content)
            mail.close()
            sofiaResponse('Your email has been sent successfully.')
        else:
            sofiaResponse('I don\'t know what you mean.')

#open an application
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open", "-n", '/Applications/' + appname1], stdout=subprocess.PIPE)

#getting weather update. Remember to look into this one deeper
    elif 'current weather' in command:
        reg_ex= re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            own = OWM(api_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='fahrenheit')
            sofiaResponse('Currently, the weather in %s is %s. Today will have a high of %d and a low of %d degrees' % (city, k, x['temp_max'], x['temp_min']))

#tells time
    elif 'time' in command:
        import datetimenow 
        now = datetime.datetime.now()
        hour=now.hour
        S_hour=(hour-12)
        minute=now.minute
        sofiaResponse('Currently it\'s %s, %s' % hour, minute)

#Sofia says hello and goodbye
    elif 'hello' in command:
        day_time= int(strftime('%H)'))
        if day_time<12:
            sofiaResponse('Good Morning!')
        elif 12<= day_time<18:
            sofiaResponse('Hi, good afternoon!')
        else:
            sofiaResponse('Good evening!')
#to terminate the program
    elif 'shutdown' in command:
        sofiaResponse('Goodbye, see you later')
        sys.exit()

#use vlc to play a song via youtube 
#     elif 'play me a song' in commmand:
#         path = '/Users/bigmac/Documents/sofiaSongs/'
#         folder = path
#         for the_file in os.listdir(folder):
#             file_path = os.path.join(folder, the_file)
#             try:
#                 if os.path.isfile(file_path):
#                     os.unlink(file_path)
#             except Exception as e:
#                 print(e)

# sofiaResponse('Which song would you like me to play?')
#             mysong = myCommand()
#                 if mysong:
#                     flag = 0
#                     url = 'https://www.youtube.com/results?search_query=' + mysong.replace('','+')
#                     response = = urllib2.urlopen(url)
#                     html = =response.read()
#                     soup1 = =soup(html, 'lxml')
#                     url_list = []
#                     for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
#                         if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):)
#                             flag = =1
#                             final_url = 'https://www.youtube.com' + vid ['href']
#                             url_list.append(final_url)

# url = url_list[0]
#         ydl_opts = {}

# os.chdir(path)
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#         vlc.play(path)

# if flag == 0:
#         sofiaResponse('I haven\'t found anything in Youtube.')

    
#change wallpaper
    # elif 'change wallpaper' in command:
    #     folder = '/Users/bigmac/Documents/wallpaper/'
    #     for the_file in os.listdir(folder):
    #         file_path = os.path.joi(folder, the_file)
    #         try:
    #             if os.path.isfile(file_path):
    #                 os.unline(file_path)
    #         except Exception as e:
    #             print(e)
    #         api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
    #         url = 'https://api.unsplash.com/photos/random?client_id=' + api_key
    #         f = irllib2.urlopen(url)
    #         json_string = f.read()
    #         f.close()
    #         parsed_json = json.loads(json_string)
    #         photo = parsed_json['urls']['full']
    #         urllib.urlretrieve(photo,'/Users/bigmac/Documents/wallpaper/') #location where we download the image to
    #         subprocess.call([killall doc], shell=True)
    #         sofiaResponse('wallpaper changed successfully')

#get you daily news
    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client,read()
            Client.close()
            soup_page = soup(xml_page,'xml')
            news_list = soup_page.findAll('item')
            for news in news_list[:15]:
                sofiaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    #use wikipedia
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                sofiaResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
            sofiaResponse(e)

    #tell a joke
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('No jokes for now')
        

    #help me
    elif 'options' in command:
            sofiaResponse("""
            You can use these commands and I'll help you out:
            1. Open reddit subreddit : Opens the subreddit in default browser.
            2. Open xyz.com : replace xyz with any website name
            3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
            4. Current weather in {cityname} : Tells you the current condition and temperture
            5. Hello
            6. play me a video : Plays song in your VLC media player
            7. change wallpaper : Change desktop wallpaper
            8. news for today : reads top news of today
            9. time : Current system time
            10. top stories from google news (RSS feeds)
            11. tell me about xyz : tells you about xyz
            """)



sofiaResponse('Robo Bobo Test')

#loop to continue the commands
while True:
    assistant(myCommand())

