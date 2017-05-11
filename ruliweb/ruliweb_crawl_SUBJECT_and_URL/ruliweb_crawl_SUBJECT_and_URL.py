import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import requests


def getTableRow(url):
    session = requests.Session()
    response = session.get(url)
    strainer = SoupStrainer()
    bsObj = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
    tablerows = bsObj.find_all("tr", {"class": "table_body"})
    target_info_arr = []
    target_url_arr = []
    for row in tablerows[2:]:
        target_info = [i.get_text().strip() for i in row.find_all('td')]
        target_url = row.find_all('td')[2].find("a").attrs["href"]
        target_info_arr.append(target_info)
        target_url_arr.append(target_url)
    return (target_info_arr, target_url_arr)


def main():
    urls = ["http://bbs.ruliweb.com/news/board/11/list?page=" + str(i) for i in range(1, 54)]
    su_target_info_arr = []
    su_target_url_arr = []
    num = 0
    for url_i in urls:
        try:
            target_info_arr, target_url_arr = getTableRow(url_i)
            su_target_info_arr += [target_info for target_info in  target_info_arr]
            su_target_url_arr += [target_url for target_url in target_url_arr]
            print(num)
            num += 1
        except:
            pass

    df1 = pd.DataFrame(su_target_info_arr)
    df2 = pd.DataFrame(su_target_url_arr)
    df1.to_excel("target_info.xlsx")
    df2.to_excel("target_url.xlsx")


if __name__== "__main__":
    main()
