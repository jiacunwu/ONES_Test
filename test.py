import json
import requests
import pymysql
import random
import os
import sys
import time


def send_message(message, member_list):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=569464bd-e522-4a8a-82a8-294c963b4595'
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


def book_time():
    while True:
        if time.strftime('%A', time.localtime(time.time())) not in ['Sunday', 'Saturday']:
            if time.strftime('%H', time.localtime(time.time())) == '11':
                if time.strftime('%M', time.localtime(time.time())) == '10':
                    send_message('点外卖了', ['@all'])
                    print(time.strftime('%H:%M', time.localtime(time.time())))
                    time.sleep(600)
                else:
                    print(time.strftime('%H:%M', time.localtime(time.time())))
                    time.sleep(60)
            elif time.strftime('%H', time.localtime(time.time())) == '18':
                if time.strftime('%M', time.localtime(time.time())) == '10':
                    send_message('登记工时', ['@all'])
                    print(time.strftime('%H:%M', time.localtime(time.time())))
                    time.sleep(600)
                else:
                    print(time.strftime('%H:%M', time.localtime(time.time())))
                    time.sleep(60)
            else:
                print(time.strftime('%H:%M', time.localtime(time.time())))
                time.sleep(60)


if __name__ == "__main__":
    book_time()
    # print(time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(int(time.time()) + 3600000)))
    # send_message('不至于不至于', [''])
