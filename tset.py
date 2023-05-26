import requests
import json
import time
import copy
from bs4 import BeautifulSoup
from datetime import datetime


url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 REST 키 값&redirect_uri=https://example.com/oauth&response_type=code
url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = 'REST API'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'code'
site_url = 'https://m.fmkorea.com/hotdeal'
board_list = []
p_board_list = []


def f_get_list():
    result_search = requests.get(site_url)
    # print(result_search)
    html = result_search.text
    soup = BeautifulSoup(html, 'html.parser')
    times = soup.select('.regdate')
    titles = soup.select('.hotdeal_var8')

    for idx in range(0, len(titles), 1):
        t = titles[idx].text.replace('\t', '')
        loc = t.rfind('[')
        board_list.append('제목:' + t[0:loc] + ' 링크:' + site_url + titles[idx]['href'])
            #'작성시간:' + times[idx].text.strip() + '  제목:' + t[0:loc] + ' 링크:' + site_url + titles[idx]['href'])


def f_auth():
    data = {
        'grant_type': 'authorization_code',
        'client_id': rest_api_key,
        'redirect_uri': redirect_uri,
        'code': authorize_code,
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    r_token = ts["refresh_token"]
    return r_token


def f_auth_refresh(r_token):
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    data = {
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": r_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    with open(r"kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    token = ts["access_token"]
    return token


def f_send_talk(token, text):
    header = {'Authorization': 'Bearer ' + token}
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    post = {
        'object_type': 'text',
        'text': text,
        'link': {
            'web_url': 'https://developers.kakao.com',
            'mobile_web_url': 'https://developers.kakao.com'
        },
        'button_title': '키워드'
    }
    data = {'template_object': json.dumps(post)}
    return requests.post(url, headers=header, data=data)


r_token = f_auth()

while True:
    f_get_list()
    token = f_auth_refresh(r_token)
    sms_list = list(set(board_list) - set(p_board_list))
    p_board_list = copy.deepcopy(board_list)
    #p_board_list = board_list 

    f_send_talk(token, '현재 시간 {} 기준 최신글은 총 {}개입니다.'.format(datetime.now().strftime('%H:%M:%S'),len(sms_list)))
    for i in range(0, len(sms_list), 1):
        f_send_talk(token, sms_list[i])

    board_list.clear()
    sms_list.clear()
    time.sleep(1800)
