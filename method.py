from copy import deepcopy

base_response = {'version': '2.0', 'template': {'outputs': [], 'quickReplies': []}}

carouselbase_response = {'version': '2.0', 'template': {'outputs': [{"carousel": {"type": "basicCard", "items": []}}],
                                                        'quickReplies': []}}


def insert_text(text):
    new_response = deepcopy(base_response)
    #new_response['template']['outputs'].append({"simpleText": {"text": text}})
    new_response['template']['outputs'] = [{"simpleText": {"text": text}}]
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
