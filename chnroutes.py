#!/usr/bin/env python

import os
import platform
import requests

def set_listfile(FILENAME="iplist"):
    my_platform = platform.system()
    if my_platform == "Windows":
        list_path = str(os.getcwd()) + "\\" + FILENAME
    else:
        list_path = "./" + FILENAME
    del my_platform
    return list_path

def get_iplist(FILENAME=set_listfile()):
    iplist_url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    if not os.path.exists(FILENAME):
        print("iplist not exist")
        data = requests.get(iplist_url)
        with open(FILENAME, "wb") as code:
            code.write(data)
    else:
        print("iplist exist")

def convert_iplist(LOCATION="CN", LISTFILE=set_listfile()):
    print()

def main():
    data = open(set_listfile())
    nu = 0
    for line in data:
        print(line)
        nu+=1
        if nu > 10:
            break

if __name__ == '__main__':
    main()
