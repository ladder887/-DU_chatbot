from flask import Flask, json, request, jsonify
import sys
from cafeteria import *
from button import *
from method import * 
from haksa import *

#from bokgjigwan import *
#from ungjigwan import *
#from test import *

app = Flask(__name__)

@app.route("/cafeteria", methods=['POST'])
def cafeteria():
    content = request.get_json()
    print(content)
    response = cafeteria_parser(content)
    return jsonify(response)

@app.route("/button", methods=['POST'])
def button():
    response = buttons()
    return jsonify(response)

@app.route("/haksa", methods=['POST'])
def haksa():
    content = request.get_json()
    response = haksa_parser(content)
    return jsonify(response)



""" # 사용안함
@app.route("/bogjigwan", methods=['POST'])
def bokgjigwan():
    response = bokgjigwan_menu()
    return jsonify(response)

@app.route("/ungjigwan", methods=['POST'])
def ungjigwan():
    response = ungjigwan_menu()
    return jsonify(response)

@app.route("/test", methods=['POST'])
def test():
    content = request.get_json() #사용자가 보낸 메세지 입력
    response = test(content)
    return jsonify(response)
"""


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
    
