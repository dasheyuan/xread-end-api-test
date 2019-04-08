import io
import json
import random
import sys
import time

import requests


def setup_io():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)


setup_io()


load_city = []
load_log = []
with open("./cities.json", "r") as f:
    load_city = json.load(f)


def test_login_api():
    appKey = "560a7c10-3975-11e9-b595-59bd75abfd86"
    appSecret = "c28c020b5e5863047aca6230728245ee"
    logs = []
    with open("./activate_log.txt", "r") as file1:
        try:
            while True:
                text_line = file1.readline()
                if text_line:
                    logs.append(text_line)
                else:
                    break
        finally:
            f.close()

    logs_len = len(logs)-1
    while True:
        index = random.randint(0, logs_len)
        one_log = json.loads(logs[index])
        if one_log['status_code'] != 200:
            print("服务器异常")
            break
        mac_str = one_log['data']['mac']
        city_str = ''
        for i in range(10000):
            if random.randint(1, 1000) < 999:
                city_str = one_log['data']['city']
            else:
                index = random.randint(0, 342)
                city_str = load_city[index]['name']

        token = one_log['data']['token']
        headers = {'Content-Type': 'application/json'}
        json_data2 = {"mac": mac_str, "city": city_str, "appKey": appKey, "token": token}
        r = requests.post('http://120.79.33.170/api/auth/login', headers=headers,
                          data=json.dumps(json_data2))
        # print(r.json())
        time.sleep(0.1)


test_login_api()

