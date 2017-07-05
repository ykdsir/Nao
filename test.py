#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from naoMotion import Motion
import cv2
from tools import htmlTools,textTools,query,voice2txt

global motion

def testSound(IP,PORT):
    global motion
    motion = Motion(IP,PORT)

    motion.recordSound("record.wav","./sound/sound.wav")
    txt = voice2txt.wav2txt('./sound/sound.wav')
    return txt
    # print pics.shape
    # print pics[0]


def testHtml(str):
    # str = '清华大学校长是？'
    # str = u'清华大学的校长是'
    str = textTools.subReplace(str)
    queryWords = textTools.wordSegment(str)
    print 'query words :  '+ queryWords.encode('utf8')
    result = query.query(queryWords)
    print 'result: ', result
    motion.say(result)

def ask(IP,PORT):
    txt = testSound(IP,PORT)
    testHtml(txt)

def takePics(IP,PORT):
    global motion
    motion = Motion(IP,PORT)
    pics = motion.takePic()
    cv2.imwrite("./pics/hu7.jpg",pics)

if __name__ == '__main__':
    IP = sys.argv[1]
    PORT = 9559
    # testSound(IP, PORT)
    ask(IP,PORT)
    # takePics(IP,PORT)