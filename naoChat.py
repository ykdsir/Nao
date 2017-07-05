# -*- coding: utf-8 -*-
import aiml,os
from tools import textTools as txtPro
from tools import query

def chat(message):
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
    respond = ''
    if message == "quit":
        exit()
    elif message == "save":
        robot.saveBrain('brain.brn')
    else:
        respond = robot.respond(message)
        print respond

    if respond.__contains__('#'):
        respond = ask(message)
    print 'chat respond:' + respond
    return respond

#问答系统
def ask(question):
    queryWords = txtPro.wordSegment(question)
    print 'query words :  '+ queryWords.encode('utf8')
    result = query.query(queryWords)
    print 'result: ', result
    pass