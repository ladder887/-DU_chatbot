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
# 학사 공지 뷴류 x
def normal_parser():
    #학사공지파싱
    url = "https://daegu.ac.kr/article/DG159/list"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    text = soup.find_all( 'tr', attrs={'class': None})
    #text.find_all('a' href="/article/DG159/detail/591560?pageIndex=1").decompose()

    # 전송 데이터 형식 설정 및 저장
    response = insert_list("대구대학교 학사공지")
    response = insert_list_button(response,"더보기","https://daegu.ac.kr/article/DG159/list")

    # 전송 데이터 형식 설정 및 저장
    for i in range(1, 5):
        onclick = re.sub(r'[^0-9]', '', text[i].find("a").attrs["onclick"])
        text[i] = list(filter(None, re.sub(' +', ' ', text[i].get_text()).replace("\r", "").split("\n")))
        post = "[{}]{}{}".format(text[i][1],text[i][5].rstrip(),text[i][6].lstrip())
        date = text[i][11]
        response = insert_list_item(response, post, date, "https://www.daegu.ac.kr/resources/images/site/layout/header_search.svg", "https://www.daegu.ac.kr/article/DG159/detail/"+onclick)

    #하단버튼추가
    reply = make_reply("전체", " 학사공지" )
    response = insert_replies(response, reply)
    for j in dict_kategorie.keys():
        reply = make_reply(j, j+" 학사공지" )
        response = insert_replies(response, reply)

    return response
# 학사 공지 뷴류o
def kategorie_parser(content):
    # 학사공지파싱
    url = "https://daegu.ac.kr/article/DG159/list?article_seq=&flag=&pageIndex=1&category_nm={}&category_cd={}&searchCondition=TA.SUBJECT&searchKeyword=".format(content, dict_kategorie[content])
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    text = soup.find_all( 'tr', attrs={'class': None})

    # 전송 데이터 형식 설정 및 저장
    response = insert_list("대구대학교 학사공지 [{}]".format(content))
    response = insert_list_button(response,"더보기","https://daegu.ac.kr/article/DG159/list?article_seq=&flag=&pageIndex=1&category_nm={}&category_cd={}&searchCondition=TA.SUBJECT&searchKeyword=".format(content, dict_kategorie[content]))

    for i in range(1, 5):
        onclick = re.sub(r'[^0-9]', '', text[i].find("a").attrs["onclick"])
        text[i] = list(filter(None, re.sub(' +', ' ', text[i].get_text()).replace("\r", "").split("\n")))
        post = "[{}]{}{}".format(text[i][1],text[i][5].rstrip(),text[i][6].lstrip())
        date = text[i][11]
        response = insert_list_item(response, post, date, "https://www.daegu.ac.kr/resources/images/site/layout/header_search.svg", "https://www.daegu.ac.kr/article/DG159/detail/"+onclick)
    
    # 하단버튼추가
    reply = make_reply("전체", " 학사공지" )
    response = insert_replies(response, reply)
    for j in dict_kategorie.keys():
        reply = make_reply(j, j+" 학사공지" )
        response = insert_replies(response, reply)

    return response


def notification_parser(content):
    # 카테고리가 없을경우 분류없이 최신학사공지
    if (content['action']['detailParams'].get('kategorie')) == None:
        response = normal_parser()

    # 카테고리가 있을경우 카테고리 관련 최신학사공지
    else:
        content = content['action']['detailParams']['kategorie']["value"]
        content = ''.join(str(e) for e in content)
        content = content.replace(" ", "")
        response = kategorie_parser(content)
    return response



    #onclick = text[i].find("a").attrs["onclick"]
    #onclick = re.sub(r'[^0-9]', '', onclick)
    #text[i] = text[i].get_text()
    #text[i] = re.sub(' +', ' ', text[i])
    #text[i] = text[i].replace("\r", "")
    #text[i] = text[i].split("\n")
    #text[i] = list(filter(None, text[i])
