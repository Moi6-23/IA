from typing import no_type_check
import jetson.inference
import jetson.utils
import numpy as np
import time 
import os 
from gtts import gTTS
import threading

speak=True
item='Welcome to My Identify. Are you ready to Rumble?'
confidence=0
itemOld=''
import cv2
width=1280
height=720
flip=2

def sayItem():
    global speak
    global item
    while True:
        if speak == True:
            output=gTTS(text=item, lang='en', slow=False)
            output.save('output.mp3')
            os.system('mpg123 output.mp3')
            speak=False
x=threading.Thread(target=sayItem, daemon=True)
x.start()


cam = cv2.VideoCapture('/dev/video0')
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
net=jetson.inference.imageNet('googlenet')
font=cv2.FONT_HERSHEY_SIMPLEX
timeMark = time.time()
fpssFilter=0



while True:
    ret, frame = cam.read()
    img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA).astype(np.float32)
    img=jetson.utils.cudaFromNumpy(img)
    if speak == False:
        classID, confidence = net.Classify(img,width,height)
        if confidence >=.5:
            item=net.GetClassDesc(classID)
            if item != itemOld:
                speak=True
        if confidence < .5:
            item='Desconocido'
        itemOld=item
    dt=time.time()-timeMark
    timeMark=time.time()
    fps=1/dt
    fpssFilter = .95*fpssFilter+0.05*fps
    cv2.putText(frame, str(round(fpssFilter,1))+'  fps  '+item+'    '+str(round(confidence,2)),(0,30),font,1,(0,0,255),2)
    cv2.imshow('nanoCma', frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1) == ord('q'):
        break
cam.relasea()
cv2.destroyAllWindows()