import requests
from bs4 import BeautifulSoup

with open("conf/proxies.conf") as input:
    proxy_server = input.read().strip()

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.72 Safari/537.36'}


def update_proxy():
    alive = 0
    proxies = list()
    all_https_proxy = requests.get(f"http://{proxy_server}/all?type=https").json()
    print(f"检测到共存在{len(all_https_proxy)}个代理池")
    for dict in all_https_proxy:
        https_proxy = dict['proxy']
        try:
            res = requests.get("https://site.ip138.com/", headers=headers,timeout=5,proxies={"https":f"http://{https_proxy}"},verify=False)
            soup = BeautifulSoup(res.text,"html.parser")
            title = soup.title.string
            if "iP反查域名" in title and https_proxy + "\n" not in proxies:
                proxies.append(https_proxy + "\n")
                alive += 1
                print(f"{https_proxy}存活性良好")
        except Exception:
            print(f"代理池{https_proxy}出错")
            requests.get(f"http://{proxy_server}/delete?proxy={https_proxy}")#删除失效代理

    with open("proxies.txt", "w+") as output:
        output.writelines(proxies)

    print(f"更新代理池完毕，存活{alive}个，已自动删除无效代理")