import datetime
import random
import sys
import io
import json


def setup_io():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)


setup_io()

load_dict = []
with open("./cities.json", "r") as f:
    load_dict = json.load(f)


def gen_mac():
    filename = 'mac-' + datetime.datetime.now().strftime("%Y-%m-%d") + '.txt'
    f1 = open(filename, 'w')
    for i in range(1000):
        mac = random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'], 12)
        mac_str = ''.join(mac)
        index = random.randint(0, 342)
        mac_str = mac_str + ' ' + load_dict[index]['code'] + ' ' + load_dict[index]['name']
        f1.write(mac_str+" \n")


gen_mac()