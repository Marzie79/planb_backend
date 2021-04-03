import requests


def make_notification(subscriber_tokens, title, body, content=None, icon=None, image=None):
    site_url = 'https://app.najva.com/notification/api/v1/notifications/'
    image = ''
    api_key = "2da3abfc-4b09-4739-b445-a71a0d0de537"
    payload = {"api_key": api_key,
               "subscriber_tokens": subscriber_tokens,
               "title": title,
               "body": body,
               "icon": image,
               "priority": "high",
               }
    headers = {'Authorization': 'Token 786d331d512a993df4cdafe24bc6c6d3d0139a0c'}
    response = requests.request("POST", site_url, data=payload, headers=headers)
    return response.text
