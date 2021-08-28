from time import ctime
from requests import get
from requests import ConnectionError
from requests import ReadTimeout
from colorama import Fore
from requests import Timeout
import argparse

proxyFlag = False

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--subfile', help='your subdomain file, note: should be one word in a line .', required=True)
parser.add_argument('-p', '--proxy', help="default is none , if you want to use tor set the port only", type=int, required=False)
parser.add_argument('-d', '--domain', help='the main domain for scanning .', required=True)
parser.add_argument("-s", '--secure', help="user 0 for http and 1 for https protocol", required=True, type=int , choices=[1,0])
arg = parser.parse_args()
sCheck = arg.secure
s = 'https://'
ns = 'http://'
start = ""
if sCheck == 0:
    start = ns
if sCheck == 1:
    start = s
proxy = arg.proxy
if proxy != None:
    proxyFlag = True
    print(Fore.LIGHTYELLOW_EX + '[*] Start requesting suing proxy on 127.0.0.1:{}'.format(proxy))

domain = arg.domain
addr = arg.subfile
subs = open('{}'.format(addr), 'r')

whiteList = []
counter = 0
round = 0
res = open('result.txt', '+a')
res.write("\n\n{}\n{}\n".format(domain, ctime()))
res.close()
for line in subs.readlines():
    line = line.strip()
    url = start+line+"."+domain
    if proxyFlag:
        pro = {"http": "socks5://127.0.0.1:{}".format(proxy), 'https': 'socks5://127.0.0.1:{}'.format(proxy)}
        try:
            round += 1
            req = get(url, proxies=pro, timeout=5)
            if req.status_code == 200:
                counter += 1
                print(Fore.LIGHTYELLOW_EX + "[*] Testing {}".format(url))
                print(Fore.LIGHTGREEN_EX + "[+] Domain {} is founded/total ({})/({})".format(url, counter, round))
                whiteList.append(whiteList)
                res = open("result.txt", "+a")
                res.write("{}\n".format(url))
                res.close()
        except:
            print(Fore.LIGHTRED_EX + "[X] Try Failed ({})".format(round))
            continue
    if not proxyFlag:
        try:
            round += 1
            req = get(url, timeout=2)
            if req.status_code == 200:
                counter += 1
                print(Fore.LIGHTYELLOW_EX + "[*] Testing {}".format(url))
                print(Fore.LIGHTGREEN_EX + "[+] Domain {} is founded/total ({})/({})".format(url, counter, round))
                whiteList.append(url)
                res = open("result.txt", "+a")
                res.write("{}\n".format(url))
                res.close()
        except:
            print(Fore.LIGHTRED_EX + "[X] Try Failed ({})".format(round))
            continue
print(Fore.LIGHTGREEN_EX + "[+] Process is Done and {} subdomain in founded".format(counter))

