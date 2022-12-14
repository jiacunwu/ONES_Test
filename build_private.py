import jenkins
import os
import time
import threading
import requests
import json


def send_message(message, member_list):
    url = send_message_url
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": message,
            "mentioned_list": member_list
        }
    }
    re1 = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(re1.json())


def build_package(branch, tar):
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    server = jenkins.Jenkins('https://cd.myones.net/', jenkins_user_name, jenkins_token_cd)

    project_name = f'development/generate-package/tar-{tar}/{branch}'
    build_history = server.get_job_info(project_name)['builds']
    if len(build_history) > 0:
        build_num_1 = server.get_job_info(project_name)['builds'][0]['number']
    else:
        build_num_1 = 0
    server.build_job(project_name)

    if build_num_1 == 0:
        while True:
            while True:
                try:
                    build_new = server.get_job_info(project_name)['builds']
                    break
                except BaseException:
                    time.sleep(10)
            if len(build_new) > 0:
                while True:
                    try:
                        build_num = server.get_job_info(project_name)['builds'][0]['number']
                        success = str(server.get_build_console_output(project_name, build_num))[-8:-1]
                        break
                    except BaseException:
                        time.sleep(10)
                if success == 'SUCCESS' or success == 'FAILURE':
                    break
                else:
                    time.sleep(10)
            else:
                time.sleep(10)
    else:
        while True:
            while True:
                try:
                    build_num = server.get_job_info(project_name)['builds'][0]['number']
                    break
                except BaseException:
                    time.sleep(10)
            if build_num != build_num_1:
                while True:
                    try:
                        success = str(server.get_build_console_output(project_name, build_num))[-8:-1]
                        break
                    except BaseException:
                        time.sleep(10)
                if success == 'SUCCESS' or success == 'FAILURE':
                    break
                else:
                    time.sleep(10)
            else:
                time.sleep(10)
    if success == 'SUCCESS':
        SUCCESS_list.append(tar)
    else:
        FAILURE_list.append(
            f'https://cd.myones.net/job/development/job/generate-package/job/tar-{tar}/job/{branch}/')


def build_image(branch, tag_list: list):
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    while True:
        try:
            server = jenkins.Jenkins('https://marsdev-ci.myones.net/', jenkins_user_name, jenkins_token_ci)
            break
        except:
            time.sleep(10)

    project_name = f'build-image-v2'
    while True:
        try:
            build_num_1 = server.get_job_info(project_name)['builds'][0]['number']
            break
        except:
            time.sleep(10)

    parameters = {'projectApiBranch': 'master',
                  'projectWebBranch': 'master',
                  'wikiApiBranch': 'master',
                  'wikiWebBranch': 'master',
                  'thirdImportTag': 'v1.0.7',
                  'devopsBranch': 'master',
                  'auditlogSyncTag': 'master',
                  'mobileWebTag': '3.6.x_integration',
                  'binlogSyncTag': 'master',
                  'ones_platform_api': 'master',
                  'ones_plugin_hostboot': 'master',
                  'ones_plugin': 'master',
                  'ones_plugin_node': 'master',
                  'enablePerformancePro': 'true',
                  'supersetBranch': 'master',
                  'biSyncBranch': 'master',
                  'project_migrations': '',
                  'wiki_migrations': '',
                  'wizEditorBranch': 'master',
                  'wizEditorConvertBranch': 'master',
                  '': '',
                  'onesAIDockerVersion': 'master',
                  'baseImageVersion': 'v1.0.19',
                  'onesDataCollectorBranch': 'master',
                  'plugin_service_proxy': 'master',
                  'mysqlOperator': 'master',
                  'kafkaBackup': 'master'
                  }
    for i in tag_list:
        parameters[change[i]] = branch
    while True:
        try:
            server.build_job(project_name, parameters)
            break
        except:
            time.sleep(10)
    while True:
        while True:
            try:
                build_num = server.get_job_info(project_name)['builds'][0]['number']
                break
            except:
                time.sleep(10)
        if build_num != build_num_1:
            break
        else:
            time.sleep(10)
    while True:
        while True:
            try:
                success = str(server.get_build_console_output(project_name, build_num))[-8:-1]
                break
            except:
                time.sleep(10)
        if success == 'SUCCESS' or success == 'FAILURE':
            break
        else:
            time.sleep(10)
    while True:
        try:
            version = str(server.get_build_console_output(project_name, build_num)).split('\n')[22][-9:]
            break
        except:
            time.sleep(10)
    if success == 'SUCCESS':
        return version
    else:
        return False


def build_install_pak(version):
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    while True:
        try:
            server = jenkins.Jenkins('https://marsdev-ci.myones.net/', jenkins_user_name, jenkins_token_ci)

            project_name = f'build-install-pak'
            build_num_1 = server.get_job_info(project_name)['builds'][0]['number']

            parameters = {'parameters': 'master',
                          'version': version,
                          'certificate': 'master_cn'}

            server.build_job(project_name, parameters)
            break
        except:
            time.sleep(10)

    while True:
        while True:
            try:
                build_num = server.get_job_info(project_name)['builds'][0]['number']
                break
            except:
                time.sleep(10)
        if build_num != build_num_1:
            break
        else:
            time.sleep(10)
    while True:
        while True:
            try:
                success = str(server.get_build_console_output(project_name, build_num))[-8:-1]
                break
            except:
                time.sleep(10)
        if success == 'SUCCESS' or success == 'FAILURE':
            break
        else:
            time.sleep(10)

    return success


def build_create_test_env(branch, version, config='--'):
    while True:
        try:
            os.environ['PYTHONHTTPSVERIFY'] = '0'
            server = jenkins.Jenkins('https://marsdev-ci.myones.net/', jenkins_user_name, jenkins_token_ci)

            project_name = f'create-test-env'
            build_num_1 = server.get_job_info(project_name)['builds'][0]['number']

            parameters = {'instance_name': branch[:6],
                          'version': version,
                          'onesConfigureInitExtraParams': config}

            server.build_job(project_name, parameters)
            break
        except:
            time.sleep(10)
    while True:
        while True:
            try:
                build_num = server.get_job_info(project_name)['builds'][0]['number']
                break
            except:
                time.sleep(10)
        if build_num != build_num_1:
            break
        else:
            time.sleep(10)
    while True:
        while True:
            try:
                success = str(server.get_build_console_output(project_name, build_num))[-8:-1]
                break
            except:
                time.sleep(10)
        if success == 'SUCCESS' or success == 'FAILURE':
            break
        else:
            time.sleep(10)

    return success


SUCCESS_list = []
FAILURE_list = []


def build_private(branch, tag_list, is_send_message=True):
    for tag in tag_list:
        thread1 = threading.Thread(target=build_package, args=(branch, tag))
        thread1.start()
    while len(SUCCESS_list) + len(FAILURE_list) != len(tag_list):
        time.sleep(10)
    if len(SUCCESS_list) != len(tag_list):
        print(f'???????????????\n{FAILURE_list}')
        if is_send_message:
            send_message(f'??????????????? \n{FAILURE_list}', [jenkins_user_name[:-8]])
        return
    print(f'SUCCESS??? {SUCCESS_list}')

    version = build_image(branch, tag_list)
    if not version:
        print(f'??????????????????')
        if is_send_message:
            send_message(f'??????????????????: \nhttps://marsdev-ci.myones.net/view/build-private-test-env/job/build-image-v2/',
                         [jenkins_user_name[:-8]])
        return
    print(f'SUCCESS build-image-v2 version: {version}')

    success = build_install_pak(version)
    if success != 'SUCCESS':
        print(f'?????????????????????')
        if is_send_message:
            send_message(f'?????????????????????: \nhttps://marsdev-ci.myones.net/view/BUILD_PACKAGE/job/build-install-pak/',
                         [jenkins_user_name[:-8]])
        return
    print(f'{success} build-install-pak')

    success = build_create_test_env(branch, version)
    if success != 'SUCCESS':
        print(f'????????????????????????')
        if is_send_message:
            send_message(f'????????????????????????: \nhttps://marsdev-ci.myones.net/view/AUTO_DEPLOY/job/create-test-env/',
                         [jenkins_user_name[:-8]])
    else:
        print('????????????')
        if is_send_message:
            send_message(f'{branch}????????????????????????', [jenkins_user_name[:-8]])
            send_message(f'??????????????????????????? \nhttps://marsdev-ci.myones.net/view/AUTO_DEPLOY/job/remove-test-env/',
                         [jenkins_user_name[:-8]])


# ??????????????????url???????????????,?????????is_send_message??????
send_message_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=569464bd-e522-4a8a-82a8-294c963b4595'
# tag?????????????????????????????????????????????????????????????????????????????????????????????
change = {'project-web': 'projectWebBranch',
          'project-api': 'projectApiBranch',
          'wiki-web': 'wikiWebBranch',
          'wiki-api': 'wikiApiBranch',
          'audit-log-sync': 'auditlogSyncTag',
          'onesconfigure_tool': 'onesAIDockerVersion'
          }
# ??????????????????jenkins????????????token?????????https://marsdev-ci.myones.net/user/***@ones.ai/configure?????????API Token
# ??????CI???CD???token??????????????????????????????
jenkins_user_name = 'wujiacun@ones.ai'
jenkins_token_ci = '11e7b38a13794c4ddd39a62fb82460fd4e'
jenkins_token_cd = '116c13ead74879ca807a992f2b605ca1aa'

if __name__ == '__main__':
    # build_private('master', [])
    # ???????????????????????????????????????????????????????????????
    build_private('P3069', ['project-web', 'project-api'], is_send_message=True)
