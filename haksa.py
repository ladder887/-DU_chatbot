import requests
from bs4 import BeautifulSoup
import time
from method import *

def haksa_parser():
    url = "https://daegu.ac.kr/schedule/detail?schedule_info_seq=1"
    response = requests.get(url)
    response.raise_for_status()

    date = time.strftime('%m', time.localtime(time.time()))
    #print(date)

    soup = BeautifulSoup(response.text, "lxml")
    text = soup.find_all(attrs={'class':'left'})
    i = 2
    schedule = []

    for text in text:
        if i % 2 == 0:
            text = text.get_text()
            num1 = text.strip()
            month = num1[0:2]
            #print(month)
        else:
            text = text.get_text()
            text = text.strip()
            num2 = text.replace("대학", "")

            if date == month:
                schedule.append(num1 + " : " + num2)
                #print(schedule)
            elif date < month:
                break;
            #print(i)

        i += 1

    title = '이번달 학사일정'
    description = schedule
    description = '\n'.join(str(e) for e in description)
    response = insert_card(title,description)
    print(response)
    return response

haksa_parser()
