import json
import time
import requests
import os


def create_pending(phone=13902995544, edition='free', language='zh', mail=''):
    time1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))

    if mail == '':
        mail = str(time1) + '@ones.ai'
    json1 = {
        "phone": f"+86{phone}"
    }
    headers = {'referer': 'https://ones.cn/project/api/project',
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain',
               'Accept-Language': f'{language}'}
    url1 = 'https://ones.cn/project/api/project' + '/auth/verify_sms'
    re1 = requests.post(url=url1, data=json.dumps(json1), headers=headers)
    print(re1.json())
    ma = input('验证码： ')
    json2 = {
        "email": mail,
        "password": "a12345678",
        "phone": f'+86{phone}',
        "phone_code": f'{ma}',
        "edition": f'{edition}'
    }
    url2 = 'https://ones.cn/project/api/project' + '/auth/create_pending_org'
    re2 = requests.post(url=url2, data=json.dumps(json2), headers=headers)
    print(re2.json())
    print('email:  ' + mail)
    print('org_uuid: ' + re2.json()['org']['org_uuid'])
    with open('/Users/lay/PycharmProjects/pythonProject/account', 'a') as f:
        f.write('saas  ' + edition + '  ')
        f.write('email: ' + str(mail) + '  ')
        f.write('org_uuid: ' + str(re2.json()['org']['org_uuid']))
        f.write('\n')


if __name__ == '__main__':
    create_pending(13902995544, 'free', mail='')
