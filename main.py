from flask import Flask, json, request, jsonify
import sys

from card import *  # 카카오톡 데이터 전송 양식
from test import *


app = Flask(__name__)

@app.route("/index", methods=['POST'])
def index():
    response = test_index()
    return response

@app.route("/new", methods=['POST'])
def new():
    response = test_new()
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
