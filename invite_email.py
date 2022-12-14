import json
import requests
import time


def login(email, password='a12345678'):
    headers = {'referer': data['referer_url'],
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain'}
    data1 = {
        "password": password,
        "email": email
    }
    url1 = f'{data["base_url"]}/auth/login'
    re1 = requests.post(url=url1, data=json.dumps(data1), headers=headers)
    print(re1.json())
    dict1 = {'uuid': re1.json()['user']['uuid'],
             'token': re1.json()['user']['token'],
             'team_uuid': re1.json()['teams'][0]['uuid']}
    print(dict1)
    return dict1


def invite_members(team_uuid, uuid, token, invite_count, license_types=(1, 2, 3)):
    license_types = list(license_types)
    headers = {'referer': data['referer_url'],
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain',
               'Ones-User-Id': uuid,
               'Ones-Auth-Token': token}

    time1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
    mail_list = []
    for i in range(invite_count):
        mail = str(time1) + str(i) + '@ones.ai'
        mail_list.append({"email": mail})
    print(mail_list)

    url1 = f'{data["base_url"]}/team/{team_uuid}/invitations/add_batch'
    data1 = {"invite_settings": mail_list, "license_types": license_types}
    re1 = requests.post(url=url1, data=json.dumps(data1), headers=headers)
    print(re1.json())


def get_invite_code(uuid, token, team_uuid):
    headers = {'referer': data['referer_url'],
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain',
               'Ones-User-Id': uuid,
               'Ones-Auth-Token': token
               }

    url1 = f'{data["base_url"]}/team/{team_uuid}/invitations'

    response = requests.get(url1, headers=headers)
    invite_code = []
    for i in response.json()['invitations']:
        if i['status'] == 1:
            list1 = [i['email'], i['code']]
            invite_code.append(list1)
    print(invite_code)
    return invite_code


def invite_join_team(uuid, token, invite_email, invite_code):
    headers = {'referer': data['referer_url'],
               'User-Agent': 'PostmanRuntime/7.29.0',
               'Content-Type': 'text/plain',
               'Ones-User-Id': uuid,
               'Ones-Auth-Token': token}
    json_data = {
        'email': invite_email,
        'password': 'a12345678',
        'name': invite_email,
        'invite_code': invite_code,
    }
    url1 = f'{data["base_url"]}/auth/invite_join_team'
    response = requests.post(url1, headers=headers, json=json_data)
    print(response.json())


def invite(email, invite_count, invite_team='', password='a12345678', license_type=(1, 2, 3)):
    """
    :param email: ???????????????
    :param invite_count: ??????????????????
    :param invite_team: ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    :param password: ??????????????????????????????????????????a12345678
    :param license_type: ?????????????????????????????????????????????
    :return: Null
    """
    user_data = login(email, password)
    if invite_team == '':
        invite_members(user_data['team_uuid'], user_data['uuid'], user_data['token'], invite_count, license_type)
        invite_code = get_invite_code(user_data['uuid'], user_data['token'], user_data['team_uuid'])
    else:
        invite_members(invite_team, user_data['uuid'], user_data['token'], invite_count, license_type)
        invite_code = get_invite_code(user_data['uuid'], user_data['token'], invite_team)
    for i in invite_code:
        invite_join_team(user_data['uuid'], user_data['token'], i[0], i[1])


# dev
branch = 'P3044'
dev = {
    'referer_url': f'https://dev.myones.net/project/{branch}',
    'base_url': f'https://devapi.myones.net/project/{branch}'
}
# preview3
preview3 = {
    'referer_url': f'https://preview3.myones.net/project',
    'base_url': f'https://preview3.myones.net/project/api/project'
}
# preview1
preview1 = {
    'referer_url': f'https://preview1.myones.net/project',
    'base_url': f'https://preview1.myones.net/project/api/project'
}
# ????????????
port = '14118'
private = {
    'referer_url': f'http://120.79.10.250/project/api/project',
    'base_url': f'http://120.79.10.250/project/api/project'
}
# SaaS
SaaS = {
    'referer_url': f'https://ones.cn/project/api/project',
    'base_url': f'https://ones.cn/project/api/project'
}

# ??????????????????
data = private

if __name__ == '__main__':
    invite(email='test@ones.ai', invite_count=80, invite_team='',
           password='test1234', license_type=(1, 2, 3, 4, 5))
