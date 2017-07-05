#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import globalVar

def wav2txt(filename):
    r = sr.Recognizer()
    with sr.WavFile(filename) as source:
        audio = r.record(source)
    try:
        text = r.recognize_ibm(audio,username = globalVar.IBM_USERNAME, password = globalVar.IBM_PASSWORD, language = 'zh-CN')
    except Exception:
        text = None
    print 'wav to text : ',text
    return text