from selenium import webdriver
from scrapy import Selector
import pandas as pd
import time
browser=webdriver.PhantomJS("D:\\game\\pythoncode\\ruliweb\\webdriver\\phantomjs\\bin\\phantomjs.exe")

def getInfoMat(url):
    browser.get(url)
    time.sleep(0.5)
    html = browser.find_element_by_xpath("//*").get_attribute('outerHTML')
    selector = Selector(text=html)
    table = selector.xpath('//ul[@class="row"]')[0]
    rows = table.xpath('.//ul[@class="game_info_list col col_10"]')
    names = []
    genres = []
    releaseDates = []
    playenv_strs = []
    ratingScores = []
    ratingAmts = []
    newPosts = []
    community_Links = []
    rating_Links = []
    for row in rows:
        name= row.xpath('.//strong[@class="name"]/text()')[0].extract().encode("utf-8")
        genre=row.xpath('.//li[@class ="game_info_list_item row"]')[0].xpath('.//span[@class="key"]')[1].xpath('.//text()')[0].extract().encode("utf-8")
        releaseDate =row.xpath('.//li[@class ="game_info_list_item row"]')[0].xpath('.//span[@class="key"]')[2].xpath('.//text()')[0].extract().encode("utf-8")
        playenv = [icon.extract().encode("utf-8") for icon in row.xpath('.//i[contains(@class,"icon")]/text()')]
        playenv_str = " ".join(playenv)
        ratingScore = row.xpath('.//strong[@class="text_medium rating"]/text()')[0].extract().encode("utf-8")
        ratingAmt = row.xpath('.//strong[contains(@style,"color")]/text()')[0].extract().encode("utf-8")
        newPost = row.xpath('.//strong[@class="text_medium"]/text()')[0].extract().encode("utf-8")
        community_Link = row.xpath('.//a[@class="community"]/@href')[0].extract().encode("utf-8")
        rating_Link = row.xpath('.//a[@class="community"]/@href')[1].extract().encode("utf-8")
        names.append(name)
        genres.append(genre)
        releaseDates.append(releaseDate)
        playenv_strs.append(playenv_str)
        ratingScores.append(ratingScore)
        ratingAmts.append(ratingAmt)
        newPosts.append(newPost)
        community_Links.append(community_Link)
        rating_Links.append(rating_Link)
    return [names,genres,releaseDates,playenv_strs,ratingScores,ratingAmts,newPosts,community_Links,rating_Links]

def main():
    urls = ["http://bbs.ruliweb.com/game/search?ordering=ranking_a&search_key=&page=%d"%(i) for i in range(1,1381)]
    info_mat = getInfoMat(urls[0])
    checker = 0
    for url in urls[1:]:
        print(checker)
        info_mat_i = getInfoMat(url)
        info_mat = [i+j for i,j in zip(info_mat,info_mat_i)]
        checker += 1
    df = pd.DataFrame({"names":info_mat[0],"genres":info_mat[1],"releaseDates":info_mat[2],"playenv_strs":info_mat[3],"ratingScores":info_mat[4],"ratingAmts":info_mat[5],"newPosts":info_mat[6],"community_Links":info_mat[7],"rating_Links":info_mat[8]}
                ,columns=["names","genres","releaseDates","playenv_strs","ratingScores","ratingAmts","newPosts","community_Links","rating_Links"])
    df.to_csv("D:\\game\\pythoncode\\ruliweb\\ruliweb_crawl_gameInfo\\gameInfo.csv",encoding="utf-8")
if __name__ =="__main__":
    main()
