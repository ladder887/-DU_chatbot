import json
import time
from method import *
import requests
import re
from datetime import date

def cafeteria_parser():
    today = date.today()
    weekday_number = today.weekday()

    if weekday_number == 6:
        weekday_number -=6
    else:
        weekday_number += 1

    #date1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    response = {
        'restaurant_seq': '2',
        'menu_date': '2023-05-19'
    }

    responses = requests.post('https://daegu.ac.kr/restaurant/menu/list', data=response)
    res = responses.json()

    title = "복지관 오늘의 식단"

    menu_total = []
    temp = res[weekday_number-1]
    #print(temp)
    temp = temp['menu_content']
    
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', temp)
    result = result.split()

    if len(result) <= 3:
        menu_total.append("등록된 식단이 없습니다")
        #print(menu_total)
    else:
        for j in range(3, len(result)):
            menu_total.append(result[j])
        #print(menu_total)

    menu = '\n'.join(str(e) for e in menu_total)
    response = insert_card(title , menu)
    #print(response)

    return response
