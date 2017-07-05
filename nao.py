# -*- coding: utf-8 -*-

import sys,time,globalVar
import naoChat,naoVision
from naoMotion import Motion
from tools import voice2txt

FACE_RECO_STATE = 0
CHAT_STATE = 1
INST_STATE = 2
currentState = FACE_RECO_STATE
motion = Motion()


# QUIT_STATE = 3
def main(ip,port):
    # currentState = FACE_RECO_STATE
    global motion
    motion = Motion(ip,port)
    __chat()
    pass

def __changeState():
    if currentState == FACE_RECO_STATE:
        __faceRecognition()
        pass
    elif currentState == CHAT_STATE:
        __chat()
        pass
    elif currentState == INST_STATE:
        __instruction()
        pass
    else:
        print 'Goodbye! '
        motion.say('再见')

def __faceRecognition():
    pass

def __chat():
    while True:
        motion.recordSound("record.wav", "./sound/sound.wav")
        text = voice2txt.wav2txt('./sound/sound.wav')
        naoChat.chat(text)
        time.sleep(globalVar.SLEEP_LENGTH)
    pass

def __instruction():
    pass

if __name__ == '__main__':
    IP = sys.argv[1]
    PORT = 9559
    main(IP, PORT)