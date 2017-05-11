import pandas as pd
from selenium import webdriver
import time
from scrapy import Selector
import re
browser = webdriver.PhantomJS("D:\\game\\pythoncode\\ruliweb\\webdriver\\phantomjs\\bin\\phantomjs.exe")
#browser = webdriver.Chrome("C:\\Users\\Yunwoo\\Desktop\\webdriver\\chromedriver.exe")

def getCommentInfo_Page():
    t1 = time.time()
    time.sleep(0.5)
    html = browser.find_element_by_xpath("//*").get_attribute('outerHTML')
    selector = Selector(text=html)

    table = selector.css('table.comment_table')
    if len(table) == 2:
        rows = table[1].xpath('.//tr[contains(@id, "ct_")]')
    elif len(table) == 1:
        rows = table[0].xpath('.//tr[contains(@id, "ct_")]')
    datetimes = []
    nicks = []
    comments = []
    likes = []
    dislikes = []
    for row in rows:
        nick = row.css('div.nick').css('strong').xpath('./text()')[0].extract().encode('utf-8')
        try:
            comment = row.css('div.text_wrapper').xpath('./span[@class="text"]/text()')[0].extract().encode('utf-8')
            comment = re.sub(r'[\n+\s+]',' ',comment)
        except:
            print('removedComment')
            comment = ""
        datetime = row.css('span.time').xpath('./text()')[0].extract().encode('utf-8')
        like = row.css('button.btn_like').xpath('./span/text()')[0].extract().encode('utf-8')
        dislike = row.css('button.btn_dislike').xpath('./span/text()')[0].extract().encode('utf-8')
        datetimes.append(datetime)
        nicks.append(nick)
        comments.append(comment)
        likes.append(like)
        dislikes.append(dislike)
    t2 = time.time()
    print(str(t2-t1))
    return [datetimes,nicks,comments,likes,dislikes]

def getCommentInfo(url):
    browser.get(url)
    try:
        Page_comment = getCommentInfo_Page()
    except:
        df = pd.DataFrame({"datetime":(["9999.9.9"]),"nicks":["nodata"],"comment":["nodata"],"like":[0],"dislike":[0]},
                          columns=["datetime","nicks","comment","like","dislike"])
        print("no comment")
        return df

    while True:
        paging = browser.find_element_by_css_selector("div.paging_wrapper.row.bottom")
        pagebtn = paging.find_elements_by_class_name("btn_num")
        if len(pagebtn) == 1:
            break
        time.sleep(0.5)
        for i in range(1,len(pagebtn)):
            pagebtn[i].click()
            Page_comment_next =  getCommentInfo_Page()
            Page_comment = [i+j for i,j in zip(Page_comment,Page_comment_next)]
            paging = browser.find_element_by_css_selector("div.paging_wrapper.row.bottom")
            pagebtn = paging.find_elements_by_class_name("btn_num")
        if len(pagebtn) != 10:
            break
        try:
            paging.find_element_by_class_name('btn_next').click()
            time.sleep(0.5)
        except:
            break
    datetime,nicks,comment,like,dislike = Page_comment[0],Page_comment[1],Page_comment[2],Page_comment[3],Page_comment[4]
    df = pd.DataFrame({"datetime":datetime,"nicks":nicks,"comment":comment,"like":like,"dislike":dislike},columns=["datetime","nicks","comment","like","dislike"])
    return df

def getTargetInfo():
    info = pd.read_excel("D:\\game\\pythoncode\\ruliweb\\ruliweb_crawl_comment\\source\\target_info.xlsx")
    return info.SUBJECT

def getTargetUrl():
    url = pd.read_excel("D:\\game\\pythoncode\\ruliweb\\ruliweb_crawl_comment\\source\\target_url.xlsx")
    return url.urls

def main():
    urlList = getTargetUrl()
    subject = getTargetInfo()
    df = getCommentInfo(urlList[0])
    pn = pd.DataFrame({"subject":[subject[0] for _ in range(len(df))]})
    df = pd.concat([df,pn],axis=1)
    checker = 0
    for url_i,subject_i in zip(urlList[1:],p_keys[1:]):
        df_i = getCommentInfo(url_i)
        pn_i = pd.DataFrame({"subject":[subject_i for _ in range(len(df_i))]})
        df_i = pd.concat([df_i,pn_i],axis=1)
        df = pd.concat([df,df_i],axis = 0)
        print(checker)
        checker += 1
    df.to_csv("D:\\game\\pythoncode\\ruliweb\\ruliweb_crawl_comment\\comment_of_review.csv")
    return 0

if __name__=="__main__":
    main()
