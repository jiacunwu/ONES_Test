import json
import requests
import time


def create_email(api_key='bHnBNUX2RJwqd8zscm3O'):
    time1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
    email = str(time1) + '@linshiyou.com'
    headers = {'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain'}
    url = f'https://youxiang.dev/api/email/{email}/{api_key}'
    re = requests.get(url, headers)
    print(re.status_code)
    print(email)
    return email


def get_email_code(email, api_key='bHnBNUX2RJwqd8zscm3O'):
    headers = {'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain'}
    url = f'https://youxiang.dev/api/messages/{email}/{api_key}'
    while True:
        re = requests.get(url, headers)
        if len(re.json()) > 0:
            print(re.json()[0]['subject'][-7:-1])
            break
        else:
            time.sleep(5)
    return re.json()[0]['subject'][-7:-1]


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
    url2 = dev_base_url + '/auth/invitation/link/verify_email'
    data2 = {"email": email, "invite_code": invite_code}
    headers2 = {"referer": dev_base_url, "Accept-Language": "cn"}
    res2 = requests.post(url=url2, data=json.dumps(data2), headers=headers2)
    print(res2.json())


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
    for i in range(invite_count):
        email = create_email()
        time.sleep(2)
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


dev_base_url = 'https://ones.cn/project/api/project'

if __name__ == '__main__':
    join_team_multi('6BEvDXkPtEK1wdUoESt69FKQ7k3HmhS7', 4)
    # user_data = login('0919150729@ones.ai')
    # get_email_code('092011@ones.ai')
    # for i in range(30):
    #     invite_code2 = reset_link(user_data['team_uuid'], user_data['uuid'], user_data['token'])
    #     join_team_multi(invite_code2, 50)
