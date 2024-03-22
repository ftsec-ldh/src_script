import requests
from bs4 import BeautifulSoup
import threading
import time

with open("conf/proxies.conf") as input:
    proxy_server = input.read().strip()#proxypool服务器

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.72 Safari/537.36'}

def check(https_proxy):
    try:
        res = requests.get("http://site.ip138.com/106.75.184.166", headers=headers, timeout=5,proxies={"http": f"http://{https_proxy}"}, verify=False)
        text = res.text
        if "www.bobty.com" in text:
            return True
        else:
            return False
    except Exception:
        return False



def thread_check_Bypool(dict,proxies):#proxypool多线程读取(字典读法)
    https_proxy = dict['proxy']
    if check(https_proxy):
        proxies.append(https_proxy + "\n")
        print(f"{https_proxy}存活性良好")
    else:
        print(f"代理池{https_proxy}出错")
        requests.get(f"http://{proxy_server}/delete?proxy={https_proxy}")  # 删除失效代理


def update_proxy_Bypool():#检测并更新proxypool代理
    proxies = []
    threads = []
    all_https_proxy = requests.get(f"http://{proxy_server}/all?type=http").json()
    print(f"检测到共存在{len(all_https_proxy)}个代理池")
    for dict in all_https_proxy:
        thread = threading.Thread(target=thread_check_Bypool,args=[dict,proxies])
        threads.append(thread)
        thread.start()
        time.sleep(0.5)

    for thread in threads:
        thread.join()

    with open("proxies.txt", "w+") as output:
        output.writelines(proxies)

    print(f"更新代理池完毕，存活{len(proxies)}个，已自动删除无效代理")


def thread_check_ByFile(proxy,proxies):#proxypool多线程读取(字典读法)
    proxy = proxy.strip()
    if check(proxy):
        print(f"代理池{proxy}存活良好")
        proxies.append(proxy + "\n")
    else:
        print(f"代理池{proxy}出错")

    with open("proxies.txt", "w+") as output:
        output.writelines(proxies)

def update_proxy_ByFile(file_name):#检测并更新文件代理
    with open(file_name,"r+") as proxies_input:
        all_proxies = proxies_input.readlines()
    proxies = []
    threads = []
    print(f"检测到共有{len(all_proxies)}个代理池")
    for proxy in all_proxies:
        thread = threading.Thread(target=thread_check_ByFile,args=[proxy,proxies])
        threads.append(thread)
        thread.start()
        time.sleep(0.8)

    for thread in threads:
        thread.join()
