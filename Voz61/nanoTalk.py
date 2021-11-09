#sudo apt-get install espeak

import os 
import pyttsx3
engie= pyttsx3.init()
engie.setProperty('rate',150)
engie.setProperty('voice','english+m1')

text='Get ready player One. The play will Rough. Are you ready to Rumble?''
engine.say(text)
engine.runAndWait()