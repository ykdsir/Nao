# -*- coding: utf-8 -*-

import jieba,re,os
import jieba.posseg as pseg


# initialize jieba
def jieba_initialize():
    jieba.load_userdict(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/conversation/QAattrdic.txt')
    jieba.initialize()


# Segment words by jieba

def wordSegment(text):
    text = text.strip()
    seg_list = jieba.cut(text)
    result = " ".join(seg_list)
    return result

# replace puncation with space
def subReplace(line):
    print 'line ', line
    print type(line)
    regex = re.compile(ur"[^\u4e00-\u9fa5a-zA-Z0-9_$#-]")
    return regex.sub(' ',line)

# tag and value
def postag(text):
    words = pseg.cut(text)
    # print type(words)
    # for w in words:
    #     print w.word, w.flag,';',
    # print '\n'
    return words
