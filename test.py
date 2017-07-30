#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,os,aiml,globalVar
from naoMotion import Motion
import cv2
from tools import textTools,query,voice2txt
from naoqi import ALBroker
import argparse,time

IP = '101.5.211.149'
PORT = 9559
# motion = Motion(IP,PORT)
motion = None
def testSound(IP,PORT):

    motion.recordSound("record.wav","./sound/sound.wav")
    txt = voice2txt.wav2txt('./sound/sound.wav')
    return txt
    # print pics.shape
    # print pics[0]


def testHtml(str):
    # str = '清华大学校长是？'
    # str = u'清华大学的校长是'
    if str is None:
        motion.say(u'我听不懂')
        return
    str = textTools.subReplace(str)
    queryWords = textTools.wordSegment(str)
    print 'query words :  '+ queryWords.encode('utf8')
    result = query.query(queryWords)

    print 'result: ', result
    if result is None:
        motion.say(u'我听不懂')
    else:
        result = textTools.subReplace(result.decode('utf8'))
        print result
        # motion.say(result)

def ask():
    # txt = testSound(IP,PORT)
    testHtml(u'中国的首都是哪里')
    # testHtml(txt)

def chat():
    os.chdir(globalVar.CHAT_PATH)
    robot = aiml.Kernel()
    robot.learn("std-startup.xml")
    robot.respond('LOAD AIML TEST1')
    while(True):
        message = raw_input("Enter your message>> ")
        if (message == 'quit'):
            break
        respond = robot.respond(message)
        print respond


def takePics():
    pics = motion.takePic()
    cv2.imwrite("./pics/hu7.jpg",pics)
#
if __name__ == '__main__':
    # global IP
    # IP = sys.argv[1]
    # global PORT
    # PORT = 9559
    # testSound(IP, PORT)
    # print 'test'
    ask()
    # takePics()
    # chat()

