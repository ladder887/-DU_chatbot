from copy import deepcopy

base_response = {'version': '2.0', 'template': {'outputs': [], 'quickReplies': []}}

carouselbase_response = {'version': '2.0', 'template': {'outputs': [{"carousel": {"type": "basicCard", "items": []}}],
                                                        'quickReplies': []}}


def insert_text(text):
    new_response = deepcopy(base_response)
    #new_response['template']['outputs'].append({"simpleText": {"text": text}})
    new_response['template']['outputs'] = [{"simpleText": {"text": text}}]
    return new_response


def insert_image(image_url, alt_text):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{"simpleImage": {"imageUrl": image_url, "altText": alt_text}}]
    return new_response

def puls_insert_image(new_response, image_url, alt_text):
    new_response['template']['outputs'].append({"simpleImage": {"imageUrl": image_url, "altText": alt_text}})
    return new_response

def insert_card(title, description, image_url=None, width=None, height=None):
    new_response = deepcopy(base_response)
    if image_url is not None:
        if width is not None and height is not None:
            new_response['template']['outputs'] = [{'basicCard': {
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url, 'fixedRatio': True, 'width': width, 'height': height},
                'buttons': []
            }}]
        else:
            new_response['template']['outputs'] = [{'basicCard': {
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url},
                'buttons': []
            }}]
    else:
        new_response['template']['outputs'] = [{'basicCard': {
            'title': title,
            'description': description,
            'buttons': []
        }}]
    return new_response

def plus_card(new_response,title, description, image_url=None, width=None, height=None):
    if image_url is not None:
        if width is not None and height is not None:
            new_response['template']['outputs'].append({'basicCard': {
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url, 'fixedRatio': True, 'width': width, 'height': height},
                'buttons': []
            }})
        else:
            new_response['template']['outputs'].append({'basicCard': {
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url},
                'buttons': []
            }})
    else:
        new_response['template']['outputs'].append({'basicCard': {
            'title': title,
            'description': description,
            'buttons': []
        }})
    return new_response

def insert_button_url(new_response, label, web_url):
    new_response['template']['outputs'][-1]['basicCard']['buttons'].append({
        "action": "webLink",
        "label": label,
        "webLinkUrl": web_url
    })
    return new_response


def insert_button_text(new_response, label, text):
    new_response['template']['outputs'][-1]['basicCard']['buttons'].append({
        "action": "message",
        "label": label,
        "messageText": text
    })
    return new_response


def insert_replies(new_response, reply):
    new_response['template']['quickReplies'].append(reply)
    return new_response


def make_reply(label, message):
    return {'action': 'message', 'label': label, 'messageText': message}

def insert_list(title):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{'listCard': {
        'header': {"title": title},
        'items': [],
        'buttons': []
    }}]
    return new_response


def insert_list_item(new_response, title, description, imageUrl, web_url):
    new_response['template']['outputs'][0]['listCard']['items'].append({
        "title": title,
        "description": description,
        "imageUrl": imageUrl,
        "link": {"web": web_url}
    })
    return new_response

def insert_list_button(new_response, label, web_url):
    new_response['template']['outputs'][0]['listCard']['buttons'].append({
        "action": "webLink",
        "label": label,
        "webLinkUrl": web_url
    })
    return new_response

def insert_carousel_card(new_response, title, description, image_url=None, width=None, height=None):
    if image_url is not None:
        if width is not None and height is not None:
            new_response['template']['outputs'][-1]['carousel']['items'].append({
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url, 'fixedRatio': True, 'width': width, 'height': height},
                'buttons': []
            })
        else:
            new_response['template']['outputs'][-1]['carousel']['items'].append({
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url},
                'buttons': []
            })
    else:
        new_response['template']['outputs'][-1]['carousel']['items'].append({
            'title': title,
            'description': description,
            'buttons': []
        })
    return new_response

def insert_carousel_button_url(new_response, label, web_url):
    new_response['template']['outputs'][-1]['carousel']['items'][-1]['buttons'].append({
        "action": "webLink",
        "label": label,
        "webLinkUrl": web_url
    })
    return new_response

def insert_carousel_button_text(new_response, label, text):
    new_response['template']['outputs'][-1]['carousel']['items'][-1]['buttons'].append({
        "action": "message",
        "label": label,
        "messageText": text
    })
    return new_response
