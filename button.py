import json
import time
from method import *
import requests
import re
from datetime import date

def buttons():
    title = '골라골라~'
    description = "학사일정 과 학사공지를 확인.\n복지관 2F 교직원 식당 및 웅지관 한식뷔페 메뉴를 확인."
    response = insert_card(title,description)
    response = insert_button_text(response, "이번달 학사일정", "학사일정")
    response = insert_button_text(response, "최근 학사공지", "학사공지")
    response = insert_button_text(response,"복지관 및 웅지관 식단표","학식메뉴")
    return response
