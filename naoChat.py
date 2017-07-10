# -*- coding: utf-8 -*-
import aiml,os
from tools import textTools
from tools import query,voice2txt


def getVoiceMsg(motion):
    motion.recordSound("record.wav", "./sound/sound.wav")
    txt = voice2txt.wav2txt('./sound/sound.wav')
    return txt




def chat(motion):
    chat_path = './conversation/'
    os.chdir(chat_path)

    robot = aiml.Kernel()
    # robot.learn("std-startup.xml")
    # robot.respond('LOAD AIML TEST1')

    if os.path.isfile("brain.brn"):
        robot.bootstrap(brainFile="brain.brn")
    else:
        robot.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        robot.saveBrain("brain.brn")

    # message = raw_input("Enter your message>> ")
    message = getVoiceMsg(motion)
    if message == None:
        motion.say(u'我听不懂')
        return
    respond = ''
    if message == "quit":#仅用于测试时
        exit()
    elif message == "save":
        robot.saveBrain('brain.brn')
    else:
        respond = robot.respond(message)
        print respond

    if respond.__contains__('#'):
        respond = ask(message,motion)
    print 'chat respond:' + respond
    return respond

#问答系统
def ask(question,motion):
    str = textTools.subReplace(question)
    queryWords = textTools.wordSegment(str)
    print 'query words :  '+ queryWords.encode('utf8')
    result = query.query(queryWords)

    print 'result: ', result
    if result is None:
        motion.say(u'我听不懂')
    else:
        result = textTools.subReplace(result)
        motion.say(result)
