# -*- coding: utf-8 -*-

import urllib,requests
from bs4 import BeautifulSoup
from urllib import quote

def get_html_baike(url):
    headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_baike = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_baike(['script', 'style', 'img', 'sup', 'b'])]
    # print(soup.prettify())
    return soup_baike

# 百度搜索
def get_html_baidu(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    soup_baidu = BeautifulSoup(requests.get(url=url, headers=headers).content.decode('utf-8'), "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_baidu(['script', 'style','img'])]
    # print(soup.prettify())
    return soup_baidu

def get_html_zhidao(url):
    headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_zhidao = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_zhidao(['script', 'style','img'])]
    # print(soup.prettify())
    return soup_zhidao

def get_html_bing(url):
    # url = 'http://global.bing.com/search?q='+word
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    soup_bing = BeautifulSoup(requests.get(url=url, headers=headers).content.decode('utf-8'), "lxml")

    # 去除无关的标签
    # [s.extract() for s in soup_bing(['script', 'style','img'])]
    return soup_bing


def get_html_bingwd(url):
    headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_bingwd = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_bingwd(['script', 'style', 'img', 'sup', 'b'])]
    # print(soup.prettify())
    return soup_bingwd