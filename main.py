from flask import Flask, json, request, jsonify
import sys
from cafeteria import *
from button import *
from method import * 
from haksa_schedule import *
from haksa_notification import *

app = Flask(__name__)

#복지관 및 웅지관 메뉴
@app.route("/cafeteria", methods=['POST'])
def cafeteria():
    content = request.get_json()
    print(content)
    response = cafeteria_parser(content)
    return jsonify(response)

#기능 모음/ 버튼
@app.route("/button", methods=['POST'])
def button():
    response = buttons()
    return jsonify(response)

#학사일정
@app.route("/haksa/schedule", methods=['POST'])
def haksa_schedule():
    content = request.get_json()
    response = schedule_parser(content)
    return jsonify(response)

#학사공지
@app.route("/haksa/notification", methods=['POST'])
def haksa_notification():
    content = request.get_json()
    response = notification_parser(content)
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
    
