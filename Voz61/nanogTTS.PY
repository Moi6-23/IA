#sudo apt install mpg123
#sudo pip3 install gTTS
import os
from typing import Text 
from gtts import gTTS
myText='Get ready player One. The play will Rough. Are you ready to Rumble?''
myOutput=gTTS(text=myText, lang='en', slow=False)
myOutput.save('talk.mp3')
os.system('mpg123 talk.mp3')