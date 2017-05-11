#-*- coding: utf-8 -*-
from selenium import webdriver
from scrapy import Selector
import pandas as pd
import time
browser = webdriver.PhantomJS("D:\\game\\pythoncode\\ruliweb\\webdriver\\phantomjs\\bin\\phantomjs.exe")

def getComment_i(cmmt):
    nick = cmmt.xpath('.//span[@class="nickname"]/text()')[0].extract().encode("utf-8")
    text = cmmt.xpath('.//span[@class="content cmtContentOne"]/text()')[0].extract().encode("utf-8")
    like = cmmt.xpath('.//span[contains(@id,"likeCmt")]/text()')[1].extract().encode("utf-8")
    dislike = cmmt.xpath('.//span[contains(@id,"disCmt")]/text()')[1].extract().encode("utf-8")
    date = cmmt.xpath('.//span[@class="date"]/text()')[0].extract().encode("utf-8")[1:-1]
    return [nick,text,like,dislike,date]

def get_commentsData(theme_i,link_i):
    browser.get(link_i)
    time.sleep(1)
    html = browser.find_element_by_xpath("//*").get_attribute('outerHTML')
    selector = Selector(text=html)
    commtsframe = selector.xpath('//div[contains(@id,"pwbbsCmt")]')
    cmmtslist = commtsframe.xpath('.//li[contains(@class,"row")]')
    nicks,texts,likes,dislikes,dates,themes = [],[],[],[],[],[]
    for cmmt in cmmtslist:
        try:
            nick,text,like,dislike,date = getComment_i(cmmt)
        except:
            nick,text,like,dislike,date = "removed","removed","0","0","9999-99-99 99:99:99"
        nicks.append(nick.strip())
        texts.append(text.strip())
        likes.append(like.strip())
        dislikes.append(dislike.strip())
        dates.append(date.strip())
        themes.append(theme_i.strip())
        print("-------------------------------------------------------------------")
        print(nick)
        print(text)
        print(like)
        print(dislike)
        print(date)
        print(theme_i)
    commentsData = [nicks,texts,likes,dislikes,dates,themes]
    browser.back()
    time.sleep(1)

    return commentsData


def get_Page_data(themes,links):
    data_mat = [[],[],[],[],[],[]]
    for theme_i,link_i in zip(themes,links):
        data_mat_i = get_commentsData(theme_i,link_i)
        data_mat = [origin+newcomer for origin,newcomer in zip(data_mat,data_mat_i)]
    return data_mat

def get_page_themes_links():
    html = browser.find_element_by_xpath("//*").get_attribute('outerHTML')
    selector = Selector(text=html)
    frame = selector.xpath('.//*[@id="webzineNewsList"]')[0]
    posts=frame.xpath('.//div[@class="content"]')
    themes = [post.xpath('.//a/text()')[0].extract().encode("utf-8") for post in posts]
    links = [post.xpath('.//span[@class ="title"]/a/@href')[0].extract().encode("utf-8") for post in posts]
    return (themes,links)

def get_SixM_pageLen():
    pagesnum = len(browser.find_elements_by_xpath('//span[@class="basetext"]/a'))
    return pagesnum

def getInfo():
    data_mat = [[],[],[],[],[],[]]
    """full data"""
    while True:

        """6month data """
        themes,links = get_page_themes_links()

        "End function condition"
        if len(themes) == 0:
            break
        data_mat_i = get_Page_data(themes,links)
        data_mat = [origin+newcomer for origin,newcomer in zip(data_mat,data_mat_i)]
        pageNums = get_SixM_pageLen()
        while pageNums>0:
            browser.find_element_by_xpath('//a[@class="nexttext"]').click()
            time.sleep(1)
            themes,links = get_page_themes_links()
            data_mat_i = get_Page_data(themes,links)
            data_mat = [origin+newcomer for origin,newcomer in zip(data_mat,data_mat_i)]
            pageNums -= 1

        """next 6month """
        browser.find_element_by_xpath('//a[@class="nexttext2"]/img').click()
        time.sleep(1)

    return data_mat
def main():
    browser.get('http://www.inven.co.kr/webzine/news/?sclass=12&page=1')
    time.sleep(1)
    data_mat = getInfo()
    df = pd.DataFrame({"nick":data_mat[0],"text":data_mat[1],"like":data_mat[2],"dislike":data_mat[3],"date":data_mat[4],"theme":data_mat[5]})
    df.to_csv("D:\\game\\pythoncode\\ruliweb\\Inven")

if __name__ == "__main__":
    main()
