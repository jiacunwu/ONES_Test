import json
import requests
import time
import pymysql
import os


def login(email, password='a12345678'):
    headers = {'referer': dev_base_url,
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain'}
    data1 = {
        "password": password,
        "email": email
    }
    url1 = f'{dev_base_url}/auth/login'
    re1 = requests.post(url=url1, data=json.dumps(data1), headers=headers)
    print(re1.json())
    dict1 = {'uuid': re1.json()['user']['uuid'],
             'token': re1.json()['user']['token'],
             'team_uuid': re1.json()['teams'][0]['uuid']}
    print(dict1)
    return dict1


def verify_email(email, invite_code):
    # os.popen('/Users/lay/Desktop/reflushRedis')
    url2 = dev_base_url + '/auth/invitation/link/verify_email'
    data2 = {"email": email, "invite_code": invite_code}
    headers2 = {"referer": dev_base_url, "Accept-Language": "cn"}
    res2 = requests.post(url=url2, data=json.dumps(data2), headers=headers2)
    print(res2.json())


def get_email_code(email):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')
    cursor = db.cursor()
    cursor.execute(f"SELECT code FROM email_code where email ='{email}' order by create_time desc limit 1;")
    result = cursor.fetchall()
    code = result[0]
    db.close()
    print(code)
    return list(code)


def join_team(email, invite_code):
    verify_email(email, invite_code)
    code = get_email_code(email)
    code = "".join(code)
    url1 = dev_base_url + '/auth/invitation/link/join_team'
    data = {
        "email": email,
        "verify_code": code,
        "user_name": "test ones",
        "password": "a12345678",
        "isAgree": True,
        "invite_code": invite_code,
        "reconfirm": False
    }
    headers = {
        "referer": dev_base_url,
        "Accept-Language": "zh"
    }
    res = requests.post(url=url1, data=json.dumps(data), headers=headers)
    print(res.json())
    # user_uuid = res.json()["login"]["user"]["uuid"]
    # em = res.json()["login"]["user"]["email"]
    # print(em)


def join_team_multi(invite_code, invite_count):
    time1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
    for i in range(invite_count):
        time.sleep(3)
        email = str(time1) + str(i) + '@ones.ai'
        join_team(email, invite_code)
        print(email)


def reset_link(team_uuid, uuid, token):
    url2 = dev_base_url + f'/team/{team_uuid}/invitation/links/reset'
    headers2 = {'referer': dev_base_url,
                'User-Agent': 'PostmanRuntime/7.29.0',
                'Content-Type': 'text/plain',
                'Ones-User-Id': uuid,
                'Ones-Auth-Token': token}
    res2 = requests.get(url=url2, headers=headers2)
    print(res2.json()['invite_code'])
    return res2.json()['invite_code']


branch = 'P3044'
dev_base_url = f'https://devapi.myones.net/project/{branch}'
database = 'project_' + branch.lower()

if __name__ == '__main__':
    join_team_multi('OtWyxwLqx164SbPrSTrsFg5rgY1eWuUB', 50)
    # user_data = login('0919150729@ones.ai')
    # get_email_code('092001@ones.ai')
    # for i in range(30):
    #     invite_code2 = reset_link(user_data['team_uuid'], user_data['uuid'], user_data['token'])
    #     join_team_multi(invite_code2, 50)
