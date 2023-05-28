import requests
from bs4 import BeautifulSoup
import time
from method import *

def haksa_parser(content):

    if any(content['action']['detailParams']) == False:
        date = int(time.strftime('%m', time.localtime(time.time())))

    else:
        content = content['action']['detailParams']['sys_date']["value"]
        content = ''.join(str(e) for e in content)
        content = content.replace(" ", "")
        #print(content)



    url = "https://daegu.ac.kr/schedule/detail?schedule_info_seq=1"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    text = soup.find_all(attrs={'class':'left'})
    i = 2
    schedule = []

    for text in text:
        if i % 2 == 0:
            text = text.get_text()
            num1 = text.strip()
            month = int(num1[0:2])
            #print(month)
        else:
            text = text.get_text()
            text = text.strip()
            num2 = text.replace("대학", "")

            if date == month or date == 13:
                schedule.append(num1 + " : " + num2)
                #print(schedule)
            elif date < month:
                break;
            #print(i)

        i += 1
    
    if date == 13:
        title = "올해 학사일정"
    else:
        title = '{}월 학사일정'.format(date)
    description = schedule
    description = '\n'.join(str(e) for e in description)
    response = insert_card(title,description)
    response = insert_button_text(response,"전체일정","올해학사일정")

    #print(response)
    return response