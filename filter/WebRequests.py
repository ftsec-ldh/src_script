import vthread
import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.72 Safari/537.36'}

@vthread.pool(500)
def web_requests(url):
    with open()
    url = url.strip()
    if "http://" not in url and "https://" not in url:
        url = "http://" + url
    res = requests.get(url,verify=False,headers=headers,timeout=10)
    status_code = res.status_code
    if status_code == 200 or status_code == 301:
