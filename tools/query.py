
# -*- coding: utf-8 -*-

import htmlTools
from urllib import quote

def query(queryStr):
    queryWords = queryStr
    answers = []
    # search in baidu
    baidu = htmlTools.get_html_baidu('https://www.baidu.com/s?wd=' + quote(queryWords.encode('utf8')))
    # print baidu
    results = baidu.find(id=1)
    # print results
    assert results is not None
    if results.attrs.has_key('mu'):
        # ##############################
        # 百度知识图谱
        r = results.find(class_='op_exactqa_s_answer')
        if r == None:
            print "百度知识图谱找不到答案"
            # continue
        else:
            # print r.get_text()
            print "百度知识图谱找到答案"
            print r.get_text().strip().encode('utf8')
            return  (r.get_text().strip())

        # ##############################
        #  百度诗词
        r = results.find(class_="op_exactqa_detail_s_answer")

        if r == None:
            print "百度诗词找不到答案"
            # continue
        else:
            # print r.get_text()
            print "百度诗词找到答案"
            print r.get_text().strip().encode('utf8')
            return (r.get_text().strip().encode('utf8'))
            # found = True

        # ##############################
        # 计算器
        if results.attrs['mu'].__contains__('http://open.baidu.com/static/calculator/calculator.html'):

            r = results.find('div').find_all('td')[1].find_all('div')[1]

            if r == None:
                print "计算器找不到答案"
                # continue
            else:
                # print r.get_text()
                print "计算器找到答案"
                return (r.get_text().strip())
                # flag = True

        # 百度知道答案
        r = results.find(class_='op_best_answer_question_link')
        if r == None:
            print "百度知道图谱找不到答案"
        else:
            print "百度知道图谱找到答案"
            url = r['href']
            zhidao_soup = htmlTools.get_html_zhidao(url)
            r = zhidao_soup.find(class_='bd answer').find('pre')
            return (r.get_text().strip().encode('utf8'))


        if results.find("h3") != None:
            # 百度知道
            if results.find("h3").find("a").get_text().__contains__(u"百度知道"):
                url = results.find("h3").find("a")['href']
                if url == None:
                    print "百度知道图谱找不到答案"
                else:
                    print "百度知道图谱找到答案"
                    zhidao_soup = htmlTools.get_html_zhidao(url)

                    r = zhidao_soup.find(class_='bd answer')
                    if r != None:
                        r = r.find('pre')
                        return (r.get_text().strip().encode('utf8'))

        # 百度百科
        if results.find("h3").find("a").get_text().__contains__(u"百度百科"):
            url = results.find("h3").find("a")['href']
            if url != None:
                print "百度百科找到答案"
                baike_soup = htmlTools.get_html_baike(url)

                r = baike_soup.find(class_='lemma-summary')
                if r != None:
                    r = r.get_text().replace("\n", "").strip()
                    return r.encode('utf8')


    # return ""
    # 获取bing的摘要
    soup_bing = htmlTools.get_html_bing('https://www.bing.com/search?q=' + quote(queryWords.encode('utf8')))
    # 判断是否在Bing的知识图谱中
    # bingbaike = soup_bing.find(class_="b_xlText b_emphText")
    bingbaike = soup_bing.find(class_="bm_box")
    flag = 0
    if bingbaike != None:
        if bingbaike.find_all(class_ = 'b_xlText b_emphText'):
            print "Bing知识图谱找到答案"
            return (bingbaike.find_all(class_="b_xlText b_emphText")[0].get_text())
        if bingbaike.find_all(class_="b_vList")[3] != None:
            # print bingbaike.find_all(class_="b_vList")[0]
            if bingbaike.find_all(class_="b_vList")[3].find("li") != None:
                print "Bing知识图谱找到答案"
                return (bingbaike.find_all(class_="b_vList")[3].get_text())
    else:
        print "Bing知识图谱找不到答案"
        results = soup_bing.find(id="b_results")
        bing_list = results.find_all('li')
        for bl in bing_list:
            temp = bl.get_text()
            if temp.__contains__(u" - 必应网典"):
                print "查找Bing网典"
                url = bl.find("h2").find("a")['href']
                if url == None:
                    print "Bing网典找不到答案"
                    continue
                else:
                    print "Bing网典找到答案"
                    bingwd_soup = htmlTools.get_html_bingwd(url)

                    r = bingwd_soup.find(class_='bk_card_desc').find("p")
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n", "").strip()
                    answers.append(r)
                    flag = 1
                    break
    print answers
    if flag == 1:
        return ''.join(answers)
