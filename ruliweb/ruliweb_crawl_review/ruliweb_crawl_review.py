from selenium import webdriver
from scrapy import Selector
import pandas as pd
import time
browser = webdriver.PhantomJS("D:\\game\\pythoncode\\ruliweb\\webdriver\\phantomjs\\bin\\phantomjs.exe")
def get_comment_data_about_the_title_row(row):
    nick = row.xpath('.//a/strong/text()').extract()[0].encode("utf-8")
    comment = row.xpath('.//span[@class="text"]/text()').extract()[0].encode("utf-8")
    date = row.xpath('.//span[@class="time"]/text()').extract()[0].encode("utf-8")
    like = row.xpath('.//button[@class="btn_like"]').xpath('.//span[@class="num"]/text()').extract()[0].encode("utf-8")
    dislike = row.xpath('.//button[@class="btn_dislike"]').xpath('.//span[@class="num"]/text()').extract()[0].encode("utf-8")
    score = row.xpath('.//span[@class="score_text"]/text()').extract()[0].encode("utf-8")

    #print(nick)
    #print(comment)
    #print(date)
    #print(like," ",dislike)
    #print(score)
    return (nick,comment,date,like,dislike,score)

def get_comment_data_about_the_title_singlepage(title):
    data_mat = [[],[],[],[],[],[],[]]
    html = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
    selector = Selector(text=html)
    frames = selector.xpath('//*[@id="game_rating"]/div[1]/div/div[3]/div[3]/div[2]/table/tbody')
    rows = frames.xpath('.//tr[contains(@class,"comment_element normal parent")]')

    for row in rows:
        #print("------------------------------------------------------------")
        #print(title)
        try:
            nick,comment,date,like,dislike,score = get_comment_data_about_the_title_row(row)
            for idx,ele in enumerate([nick,comment,date,like,dislike,score,title]):
                data_mat[idx].append(ele)
        except:
            pass

    return data_mat

def get_comment_data_about_the_title(url,title):
    data_mat = [[],[],[],[],[],[],[]]
    browser.get(url)
    time.sleep(0.5)
    while True:
        """get first page"""
        data_mat_i = get_comment_data_about_the_title_singlepage(title)
        data_mat = [origin+new for origin,new in zip(data_mat,data_mat_i)]
        if len(data_mat[0]) == 0:
            data_mat = [["no_data"],["no_data"],["99.01.01 00:00"],["0"],["0"],["0"],[title]]
            return data_mat
        pagesToGo = browser.find_element_by_xpath('.//div[@class="paging_wrapper bottom row"]').find_elements_by_xpath('.//a[@class = "btn_num"]')
        pageNum = len(pagesToGo)
        pagesToGoIDX = 0
        while pageNum >0:
            pagesToGo = browser.find_element_by_xpath('.//div[@class="paging_wrapper bottom row"]').find_elements_by_xpath('.//a[@class = "btn_num"]')
            pagesToGo[pagesToGoIDX].click()
            time.sleep(0.5)
            data_mat_i = get_comment_data_about_the_title_singlepage(title)
            data_mat = [origin+new for origin,new in zip(data_mat,data_mat_i)]
            pageNum -= 1
            pagesToGoIDX += 1
        try:
            browser.find_element_by_xpath('.//i[@class="icon-chevron-right"]').click()
            time.sleep(0.5)
        except:
            break
    return data_mat

def get_full_data(titleList,urlList):
    data_mat = [[],[],[],[],[],[],[]]
    n = len(titleList)
    for title,url in zip(titleList,urlList):
        data_mat_i = get_comment_data_about_the_title(url,title)
        data_mat = [origin+new for origin,new in zip(data_mat,data_mat_i)]
        print(n)
        n -= 1

    return data_mat

def get_TITLE_URL():
    df = pd.read_csv("D:\\game\\pythoncode\\ruliweb\\ruliweb_crawl_review\\source\\gameInfo.csv")
    titleList = df.names
    urlList = df.rating_Links
    return (titleList,urlList)

def main():
    titleList,urlList = get_TITLE_URL()
    data_mat = get_full_data(titleList,urlList)
    df = pd.DataFrame({"nick":data_mat[0],"comment":data_mat[1],"date":data_mat[2],"like":data_mat[3],"dislike":data_mat[4],"score":data_mat[5],"title":data_mat[6]})
    df = df.drop_duplicates(["nick","comment","title"])
    df.to_excel("D:\\game\\pythoncode\\ruliweb\\ruliweb_crawl_review\\ruli_review.xlsx")

if __name__ == "__main__":
    main()
