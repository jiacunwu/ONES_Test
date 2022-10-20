import json
import sys
import time
import pymysql

import requests
import os


def get_phone_code(phone):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')
    cursor = db.cursor()
    phone = '+86' + str(phone)

    sql = f"SELECT code FROM phone_code WHERE phone='{phone}' order by create_time desc limit 1"
    print(sql)

    cursor.execute(sql)
    result = cursor.fetchall()
    code = result[0][0]
    print(code)
    db.close()
    return code


def create_pending(edition='free', mail=''):
    time1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
    if mail == '':
        mail = str(time1) + '@ones.ai'
    phone = '1' + str(time1)
    json1 = {
        "phone": f"+86{phone}"
    }
    headers = {'referer': dev_base_url,
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain',
               'Accept-Language': 'zh'}
    url1 = dev_base_url + '/auth/verify_sms'
    os.popen('/Users/lay/Desktop/reflushRedis')
    re1 = requests.post(url=url1, data=json.dumps(json1), headers=headers)
    print(re1.json())
    ma = get_phone_code(int(phone))
    json2 = {
        "email": mail,
        "password": "a12345678",
        "phone": f'+86{phone}',
        "phone_code": f'{ma}',
        "edition": f'{edition}'
    }
    url2 = dev_base_url + '/auth/create_pending_org'
    re2 = requests.post(url=url2, data=json.dumps(json2), headers=headers)
    print(re2.json())
    print('email:  ' + mail)
    print('org_uuid: ' + re2.json()['org']['org_uuid'])
    with open('/Users/lay/PycharmProjects/pythonProject/account', 'a') as f:
        f.write(f'{branch}  ' + edition + '  ')
        f.write('email: ' + str(mail) + '  ')
        f.write('org_uuid: ' + str(re2.json()['org']['org_uuid']))
        f.write('\n')


def create_org(mail=''):
    time1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
    if mail == '':
        mail = str(time1) + '@ones.ai'
    phone = '1' + str(time1)
    json1 = {
        "phone": f"+86{phone}"
    }
    headers = {'referer': dev_base_url,
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain',
               'Accept-Language': 'zh'}
    url1 = dev_base_url + '/auth/verify_sms'
    os.popen('/Users/lay/Desktop/reflushRedis')
    re1 = requests.post(url=url1, data=json.dumps(json1), headers=headers)
    print(re1.json())
    ma = get_phone_code(int(phone))
    json2 = {
        "phone": f'+86{phone}',
        "phone_code": f'{ma}',
        "name": "吴帅",
        "referrer": "",
        "keyword": "",
        "channel": "",
        "email": mail,
        "password": "a12345678",
        "team_name": "ones",
        "team_role": "CTO",
        "team_scale": "10 人以下",
        "industry": "互联网"
    }
    url2 = dev_base_url + '/auth/create_team'
    re2 = requests.post(url=url2, data=json.dumps(json2), headers=headers)
    print(re2.json())
    print('email:  ' + mail)
    print('org_uuid: ' + re2.json()['org']['uuid'])
    with open('/Users/lay/PycharmProjects/pythonProject/account', 'a') as f:
        f.write(f'{branch}  ' + 'trial' + '  ')
        f.write('email: ' + str(mail) + '  ')
        f.write('org_uuid: ' + str(re2.json()['org']['uuid']))
        f.write('\n')


branch = 'P1069'
dev_base_url = f'https://devapi.myones.net/project/{branch}'
database = 'project_' + branch.lower()

if __name__ == '__main__':
    # create_org()
    # create_pending('trial')
    create_org()
    # get_phone_code(13902995544)
