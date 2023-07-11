
import requests
token = '6396937914:AAGHJaqKDhFLZmk2tMUUzOVV0Hvqi1690i0'
method = 'sendMessage'    
response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
        data={'chat_id': '-914024384', 'text': 'hello friend'}
    ).json()