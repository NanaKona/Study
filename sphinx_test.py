import os
import speech_recognition as sr


r=sr.Recognizer()
mic=sr.Microphone()

print('I work')

with mic as source:
    r.adjust_for_ambient_noise(source)
    audio=r.listen(source)
    print('Converting text to speech...')
    print('you said '+ r.recognize_sphinx(audio))
    




# print('Time to test')
# print('...')

# for phrase in LiveSpeech():
#     print(phrase)
