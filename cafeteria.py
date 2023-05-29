import json
import time
from method import *
import requests
import re
from datetime import date

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

#당일 메뉴
def today_menu(place):
    # 복지관 웅지관 구분
    if place == "복지관":
        num = 2
        title = "복지관2F 교직원 오늘의 식단"
    elif place == "웅지관":
        num = 3
        title = "웅지관1F 한식뷔페 오늘의 식단"

    # 요일 구분
    today = date.today()
    weekday_number = today.weekday()  # 월요일 0 일요일 6
    date1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    
    if weekday_number == 6:
        weekday_number -=6
    else:
        weekday_number += 1

    # 대구대 서버에 학식 데이터 요청
    send = {
        'restaurant_seq': num,
        'menu_date': date1
    }

    data1 = requests.post('https://daegu.ac.kr/restaurant/menu/list', headers = headers, data=send)
    res = data1.json()

    # 해당요일 메뉴 데이터 저장
    menu_total = []
    temp = res[weekday_number-1]
    temp = temp['menu_content']

    # 데이터 전처리
    hangul = re.compile('[^ ㄱ-ㅣ가-힣+]+') # 한글과 띄어쓰기를 제외한 모든 글자
    result = hangul.sub('', temp) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
    result = result.split()

    if len(result) <= 3:
        menu_total.append("등록된 식단이 없습니다")
    else:
        for j in range(3, len(result)):
            menu_total.append(result[j])

    # 전송 데이터 형식 설정
    menu = '\n'.join(str(e) for e in menu_total)
    response = insert_card(title , menu)
    response = insert_button_text(response, "이번주 식단", "이번주 {}식단".format(place))
    reply = make_reply('복지관', '복지관')
    response = insert_replies(response, reply)
    reply = make_reply('웅지관', '웅지관')
    response = insert_replies(response, reply)

    return response

# 일주일 메뉴
def week_menu(place):
    # 복지관 웅지관 구분
    if place == "복지관":
        num = 2
        title = "복지관2F 교직원 이번주 식단"
    elif place == "웅지관":
        num = 3
        title = "웅지관1F 한식뷔페 이번주 식단"
        
    # 요일 구분
    today = date.today()
    date1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    dateDict = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}

    # 대구대 서버에 학식 데이터 요청
    send = {
        'restaurant_seq': num,
        'menu_date': date1
    }

    data1 = requests.post('https://daegu.ac.kr/restaurant/menu/list', headers = headers, data=send)
    res = data1.json()

    # 전송 데이터 형식 설정
    response = {'version': '2.0', 'template': {
        'outputs': [{"simpleText": {"text": title}},
                    {"carousel": {"type": "basicCard", "items": []}}], 'quickReplies': []}}
    
    for weekday in range(len(res)):
        menu_total = []
        temp = res[weekday]
        temp = temp['menu_content']
        hangul = re.compile('[^ ㄱ-ㅣ가-힣+]+') # 한글과 띄어쓰기를 제외한 모든 글자
        result = hangul.sub('', temp) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
        result = result.split()

        if len(result) <= 3:
            menu_total.append("등록된 식단이 없습니다")
        else:
            for j in range(3, len(result)):
                menu_total.append(result[j])

        menu = '\n'.join(str(e) for e in menu_total)
        response = insert_carousel_card(response,"({})".format(dateDict[weekday]), menu)
    reply = make_reply('복지관', '복지관')
    response = insert_replies(response, reply)
    reply = make_reply('웅지관', '웅지관')
    response = insert_replies(response, reply)

    return response

#메인함수
def cafeteria_parser(content):
    # 사용자가 위치 미선택시
    if (content['action']['detailParams'].get('place_cafeteria')) == None:
        response  = insert_text("복지관 또는 웅지관을 선택해주세요")
        reply = make_reply('복지관', '복지관')
        response = insert_replies(response, reply)
        reply = make_reply('웅지관', '웅지관')
        response = insert_replies(response, reply)
        return response
    
    # 사용자 이벤트 처리
    place = content['action']['detailParams']['place_cafeteria']["value"]
    place = ''.join(str(e) for e in place)
    place = place.replace(" ", "")

    # 복지관 또는 웅지관을 제외한 다른 선택시
    if place not in ["복지관", "웅지관"]:
        response  = insert_text("복지관 또는 웅지관을 선택해주세요")
        reply = make_reply('복지관', '복지관')
        response = insert_replies(response, reply)
        reply = make_reply('웅지관', '웅지관')
        response = insert_replies(response, reply)
        return response

    # 날짜 미선택 또는 당일 선택시 당일 메뉴 출력
    if (content['action']['detailParams'].get('sys_date')) == None:
        response  = today_menu(place)
    # 이번주 학식 출력
    else:
        date = content['action']['detailParams']['sys_date']["value"]
        date = ''.join(str(e) for e in date)
        date = date.replace(" ", "")
        if date == '이번주':
            response = week_menu(place)
        else:
            response  = today_menu(place)
    return response 
