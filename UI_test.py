from flask import Flask, request, jsonify, json
app = Flask(__name__)

@app.route("/keyboard")
def keyboard():
  response = {
    "type": "button",
    "buttons": [홈버튼]
  }
  return jsonify(response)
@app.route("message",methods =["post"])
def message():
  data = json.loads(request.data)
  content = data["content"]
  
  
  if content == u"홈버튼":
    response = {
      "message" : {
        "text" : "도움이 필요한 메뉴를 선택해주십시오"
      },
      "keyborad" : {
        "type" : "buttons",
        "buttons" : ["교직원 식당 메뉴", "학과공지", "오늘의 점심 추천","홈버튼"]
      }
    }
    
   elif content == u"교직원 식당 메뉴":
    response = {
      "message" : {
        "text" : "오늘 교직원 식당의 메뉴입니다."                                    #교직원 식당메뉴 추출 필요
      },
      "keyboard" : {
        "type" : "buttons",
        "buttons" : ["홈버튼"]
      }
    }
    
    elif content == u"학과 공지":
      response == {
        "message" : {
          "text" : "학과 공지입니다."                                                #학과 공지를 제목만 가져와서 선택하면 링크할 수 있나?
        }                                                                           #massage_button이나 photo로?
      }
      return jsonify(response)
        
