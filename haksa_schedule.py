import requests
from bs4 import BeautifulSoup
import time
from method import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}
# 월간 일정
def month_parser(date):
    # 대구대 학사일정 파싱
    url = "https://daegu.ac.kr/schedule/detail?schedule_info_seq=1"
    data = requests.get(url, headers=headers)
    data.raise_for_status()

    soup = BeautifulSoup(data.text, "lxml")
    temp = soup.find_all(attrs={'class':'left'})

    count = 2
    schedule = []

    # 필요한 데이터 구분 및 리스트 저장
    for text in temp:
        if count % 2 == 0:
            text = text.get_text()
            num1 = text.strip()
            month = int(num1[0:2])
        else:
            text = text.get_text()
            text = text.strip()
            num2 = text.replace("대학", "")

            if date == month or date == 13:
                schedule.append(num1 + " : " + num2)
            elif date < month:
                break;

        count += 1
        
    # 전송 데이터 형식 설정 및 저장
    title = '-{}월 학사일정-'.format(date)
    schedule = '\n'.join(str(e) for e in schedule)
    if schedule == '':
        schedule = '학사일정이 없습니다'
    response = insert_card(title,schedule)
    response = insert_button_text(response,"전체일정","올해학사일정")
    for j in range(1, 13):
        reply = make_reply('{}월'.format(j), '{}월 학사일정'.format(j) )
        response = insert_replies(response, reply)

    return response

# 해당 년도
def all_parser(date):
    # 대구대 학사일정 파싱
    url = "https://daegu.ac.kr/schedule/detail?schedule_info_seq=1"
    data = requests.get(url, headers=headers)
    data.raise_for_status()

    soup = BeautifulSoup(data.text, "lxml")
    temp = soup.find_all(attrs={'class':'left'})

    count = 2

    response = {'version': '2.0', 'template': {
        'outputs': [{"simpleText": {"text": "올해 학사일정"}},
                    {"carousel": {"type": "basicCard", "items": []}}], 'quickReplies': []}}

    #필요한 데이터 구분 및 리스트 저장
    for i in range(1, date):
        schedule = []
        for text in temp:
            if count % 2 == 0:
                text = text.get_text()
                num1 = text.strip()
                month = int(num1[0:2])
            else:
                text = text.get_text()
                text = text.strip()
                num2 = text.replace("대학", "")

                if i == month:
                    schedule.append(num1 + " : " + num2)
                elif date < month:
                    break;
            count += 1

        # 전송 데이터 형식 설정 및 저장
        schedule = '\n'.join(str(e) for e in schedule)
        if schedule == '':
            schedule = '학사일정이 없습니다'
        response = insert_carousel_card(response,"-{}월 학사일정-".format(i), schedule)
    for j in range(1, 13):
        reply = make_reply('{}월'.format(j), '{}월 학사일정'.format(j) )
        response = insert_replies(response, reply)
    return response

# 사용자 입력데이터에 따른 호출
def schedule_parser(content):
    # 날짜 데이터가 없을경우 이번달 일정 출력
    if (content['action']['detailParams'].get('sys_date')) == None:
        date = int(time.strftime('%m', time.localtime(time.time())))
        response = month_parser(date)

    # 날짜 데이터가 있을경우
    else:
        content = content['action']['detailParams']['sys_date']["value"]
        content = ''.join(str(e) for e in content)
        content = content.replace(" ", "")
        # 해당년도 일정 출력
        if content == u"올해":
            date = 13
            response = all_parser(date)
        # 입력한 달 일정 출력
        elif u'월' in content:
            date = int(content.replace("월", ""))
            response = month_parser(date)
        # 해당하는날짜 데이터가 아닐경우 이번달 일정 출력
        else:
            date = int(time.strftime('%m', time.localtime(time.time())))
            response = month_parser(date)
    

    return response