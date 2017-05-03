import pandas as pd
from selenium import webdriver
import time
#browser = webdriver.PhantomJS("C:\\Users\\namyunwoo\\webdriver\\phantomjs\\bin\\phantomjs.exe")
browser = webdriver.Chrome("C:\\Users\\namyunwoo\\webdriver\\chromedriver.exe")

def getCommentInfo_Page():
    t1 = time.time()
    model = browser.find_element_by_class_name("comment_view_wrapper")
    datetime = [i.text for i in model.find_elements_by_class_name("time")]
    nicks = [i.text for i in model.find_elements_by_class_name("nick")]
    comments = [i.text for i in model.find_elements_by_class_name("text")]
    like = [i.text for i in model.find_elements_by_class_name("btn_like")]
    dislike = [i.text for i in model.find_elements_by_class_name("btn_dislike")]
    print(t2-t1)
    return [datetime,nicks,comments,like,dislike]

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
        time.sleep(0.5)
        for i in range(1,len(pagebtn)):
            pagebtn[i].click()
            time.sleep(0.5)
            Page_comment_next =  getCommentInfo_Page()
            Page_comment = [i+j for i,j in zip(Page_comment,Page_comment_next)]
            paging = browser.find_element_by_css_selector("div.paging_wrapper.row.bottom")
            pagebtn = paging.find_elements_by_class_name("btn_num")
        try:
            paging.find_element_by_class_name('btn_next').click()
            time.sleep(0.5)
        except:
            break

    datetime,nicks,comment,like,dislike = Page_comment[0],Page_comment[1],Page_comment[2],Page_comment[3],Page_comment[4]
    df = pd.DataFrame({"datetime":datetime,"nicks":nicks,"comment":comment,"like":like,"dislike":dislike},columns=["datetime","nicks","comment","like","dislike"])
    return df


def getTargetInfo():
    info = pd.read_excel("target_info.xlsx")
    return info.P_KEY

def getTargetUrl():
    url = pd.read_excel("target_url.xlsx")
    return url.urls

def main():
    urlList = getTargetUrl()
    p_keys = getTargetInfo()
    df = getCommentInfo(urlList[0])
    pn = pd.DataFrame({"POSTNUM":[p_keys[0] for _ in range(len(df))]})
    df = pd.concat([df,pn],axis=1)
    checker = 0
    for url,pkey in zip(urlList[1:],p_keys[1:]):
        try:
            df_i = getCommentInfo(url)
        except:
            print(url)
        pn_i = pd.DataFrame({"POSTNUM":[pkey for _ in range(len(df_i))]})
        df_i = pd.concat([df_i,pn_i],axis=1)
        df = pd.concat([df,df_i],axis = 0)
        print(checker)
        checker += 1
    df.to_excel("commentData.xlsx")

if __name__=="__main__":
    main()
