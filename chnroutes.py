#encoding: utf-8
import os
import math
import platform
import requests

def add_one(ori_str):
    a = int(ori_str)
    b = a + 1
    return str(b)

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
    data = open(LISTFILE,"r")
    regex_str = "%s|ipv4" %(LOCATION)
    print(regex_str)
    ipdata = []
    for line in data:
        if line.find(regex_str) != -1:
            ipdata.append(line)


    results = []
    for item in ipdata:
        unit_items = item.split('|')
        starting_ip = unit_items[3]
        num_ip = int(unit_items[4])

        imask = 0xffffffff ^ (num_ip - 1)
        imask = hex(imask)[2:]

        mask = [imask[i:i + 2] for i in range(0, 8, 2)]
        mask = '.'.join([str(int(i, 16)) for i in mask])

        cidr = 32 - int(math.log(num_ip, 2))

        results.append((starting_ip, mask, cidr))

    return results

def convert_ipdata(ipdate):
    rules = open("chnroute.action", "w")
    for ip, mask, cidr in ipdate:
        a, b, c ,d = ip.split('.')
        if cidr > 24:
            total = 2**(24-cidr)
            while total > 0:
                total-=1
                record = "%s.%s.%s.%s/\n" %(a, b, c, d)
                d = add_one(d)
        elif cidr > 16:
            total = 2**(24-cidr)
            while total > 0:
                total-=1
                record = "%s.%s.%s.*/\n" %(a, b, c)
                c = add_one(c)
        elif cidr > 8:
            total = 2**(16-cidr)
            while total > 0:
                total-=1
                record = "%s.%s.*.*/\n" %(a, b)
                b = add_one(b)
        elif cidr > 4:
            total = 2**(8-cidr)
            while total > 0:
                total-=1
                record = "%s.*.*.*/\n" %(a)
                a = add_one(a)
        rules.write(record)
    rules.close()

def main():
    convert_ipdata(convert_iplist())

if __name__ == '__main__':
    main()
