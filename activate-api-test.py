import hashlib
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


def read_mac_code():
    macList = []
    with open("mac-2019-03-18.txt", 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            device = lines.split(" ")
            device.pop()
            macList.append(device)
    return macList


def test_activate_api():
    appKey = "560a7c10-3975-11e9-b595-59bd75abfd86"
    appSecret = "c28c020b5e5863047aca6230728245ee"
    f1 = open("./activate_log.txt", 'w')
    macList = read_mac_code()

    for i in range(len(macList)):
        mac_str = macList[i][0]
        city_str = macList[i][2]
        timestamp = int(time.time())
        randomNum = random.randint(10000, 99999)
        signature = appSecret + (str(timestamp)) + (str(randomNum))
        signature_sha1 = hashlib.sha1(signature.encode("utf8")).hexdigest()
        json_data1 = {"mac": mac_str, "city": city_str, "appId": "001001001",
                      "appKey": appKey, "timestamp": timestamp, "randomNum": randomNum,
                      "signature": signature_sha1}
        headers = {'Content-Type': 'application/json'}
        r = requests.post('http://120.79.33.170/api/auth/activate', headers=headers, data=json.dumps(json_data1))
        # token = json.loads(r.content)["data"]["token"]
        # json_data2 = {"mac": mac_str, "city": city_str, "appKey": appKey,
        #              "token": token}
        # r = requests.post('http://http://120.79.33.170/api/auth/login', headers=headers, data=json.dumps(json_data2))
        print(r.json())
        f1.write(json.dumps(r.json(), ensure_ascii=False) + ' \n')
        time.sleep(0.1)
    f1.close()


test_activate_api()