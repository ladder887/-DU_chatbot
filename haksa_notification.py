import requests
from bs4 import BeautifulSoup
from method import *
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

dict_kategorie = {"수업학적" : 1, "장학" : 2, "등록" : 3, "복지" : 4, "교육봉사" : 5, "도서관" : 7, "학생모집" : 8, "예비군" : 9, "행정안내" : 10}

def normal_parser():
    #대구대 학사일정 파싱
    url = "https://daegu.ac.kr/article/DG159/list"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    text = soup.find_all( 'tr', attrs={'class': None})
    #text.find_all('a' href="/article/DG159/detail/591560?pageIndex=1").decompose()



    response = insert_list("대구대학교 학사공지")
    response = insert_list_button(response,"더보기","https://daegu.ac.kr/article/DG159/list")

    for i in range(1, 5):
        onclick = re.sub(r'[^0-9]', '', text[i].find("a").attrs["onclick"])
        text[i] = list(filter(None, re.sub(' +', ' ', text[i].get_text()).replace("\r", "").split("\n")))
        post = "[{}]{}{}".format(text[i][1],text[i][5].rstrip(),text[i][6].lstrip())
        date = text[i][11]
        response = insert_list_item(response, post, date, "https://www.daegu.ac.kr/resources/images/site/layout/header_search.svg", "https://www.daegu.ac.kr/article/DG159/detail/"+onclick)

    for j in dict_kategorie.keys():
        reply = make_reply(j, j+" 학사공지" )
        response = insert_replies(response, reply)

    return response