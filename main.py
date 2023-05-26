from flask import Flask, json, request, jsonify
import sys
from cafeteria import *
from method import *

app = Flask(__name__)

@app.route("/haksic", methods=['POST'])
def haksic():
    response = cafeteria_parser()
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
