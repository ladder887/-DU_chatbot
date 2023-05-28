from flask import Flask, json, request, jsonify
import sys
from cafeteria import *
from button import *
from method import * 
from haksa import *

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



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
    
