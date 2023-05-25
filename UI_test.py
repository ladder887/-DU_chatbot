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
        "text" : "도움이 필요한 메뉴를 선택해 주십시오"
      },
      "keyborad" : {
        "type" : "buttons",
        "buttons" : ["복지관 식당 메뉴", "학과공지", "오늘의 점심 추천", "홈버튼"]
      }
    }
    
  elif content == u"복지관 식당 메뉴":
    response = {
      "message" : {
        "text" : "복지관 식당의 메뉴입니다."                                    #메뉴를 무슨 자료형이든 우리가 저장 or 긁어오기(텍스트, 텍스트 이미지)*메뉴판 사진은 별로일 듯
        
      },
      "keyboard" : {
        "type" : "buttons",
        "buttons" : ["오늘의 점심 추천", "홈버튼"]
      }
    }
  elif content == u"학과 공지":
    response == {
      "message" : {
        "text" : "학과 공지입니다."                                            #학과 공지를 제목만 가져와서 선택하면 링크할 수 있나?
      },                                                                      #massage_button(공지글로 가는 url), photo(공지 사진)
      "keyboard" : {
        "type" : "buttons",
        "buttons" : ["홈버튼"]
      }
    }
  elif content == u"오늘의 점심 추천":
    response == {
      "message" : {
        "text" : ""                                                          #랜덤 함수사용?       
      },
      "keyboard" : {
        "type" : "buttons",
        "buttons" : ["홈버튼"]
      }
    }
    
  
      return jsonify(response)
        
