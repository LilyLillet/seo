import requests
# https://yandex.ru/dev/id/doc/ru/codes/screen-code

# Получаем код

# https://oauth.yandex.ru/client/0183542bd8934004930fb73bf59c6dbd

client_id = '0183542bd8934004930fb73bf59c6dbd'

client_secret = ''

redirect_url= 'https://oauth.yandex.ru/verification_code'

code_url = f'https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_url}'
# Идём по урлу для получения кода
print(code_url)

code = ''
token_req_test = f'https://oauth.yandex.ru/token'
body = {
    'grant_type':'authorization_code',
    'code':code,
    'client_id':client_id,
    'client_secret':client_secret
}
g = requests.post(token_req_test,data=body )
g.text