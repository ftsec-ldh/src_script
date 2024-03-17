#从IP或域名列表中快速提取关键部分
import platform,time,socket,urllib3,requests,re,random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

system = platform.system()

if system =="Windows":
    driver_path = r'drivers\win64\chromedriver.exe'
if system =="Linux":
    driver_path = r'drivers\linux64\chromedriver'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.72 Safari/537.36'}

api_url = "https://www.aizhan.com/cha/"#查权重的接口
api_url2 = "https://site.ip138.com/"#反查域名的接口
api_url3 = "https://aiqicha.baidu.com/s?q="#查公司注册资金的接口

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


s = Service(driver_path)
driver = webdriver.Chrome(service=s, options=chrome_options)

def get_ip_address(domain):#ping功能，反查域名再正向解析判断域名是否真的绑定了IP
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "Error: Unable to resolve domain"

#获取单位名称
def get_company(url):
    url = get_main(url)
    url = api_url + url

    driver.get(url)
    text = driver.page_source

    name = re.findall(r"<span id=\"icp_company\">(.*?)</span></li>",text)
    name = ''.join(name)
    return name


    #return name,money

#获取权重
def get_rank(url):
    url = get_main(url)
    url = api_url + url

    driver.get(url)
    text = driver.page_source

    rank_bd = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/br/(.*?).png", text))
    rank_yd = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/mbr/(.*?).png", text))
    rank_360 = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/360/(.*?).png", text))
    rank_sm = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/sm/(.*?).png", text))
    rank_sg = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/sr/(.*?).png", text))
    rank_gg = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/pr/(.*?).png", text))

    return rank_bd,rank_yd,rank_360,rank_sm,rank_sg,rank_gg


def get_main(url):#获取关键域名和IP的部分
    if "http://" not in url and "https://" not in url:#fofa导出来的只有https://没有http://...大无语
        url = "http://" + url
    rule = re.search(r"\b\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\b", url)
    if rule:#返回true，说明输的是IP则提取IP关键部分，否则提取关键域名
        url = re.findall(r"\b\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\b",url)
        url = ''.join(url)
    else:
        url = re.findall(r"https?://([^:/]+)",url)
        url = ''.join(url)
    return url


def get_domain_byIP(ip):
    time.sleep(2)#防止被拉黑
    with open("proxies.txt","r+") as input:
        proxies = input.readlines()

    proxy = random.choice(proxies)

    ip = get_main(ip)
    url = api_url2 + ip
    html = requests.get(url,headers=headers,proxies={"https":f"http://{proxy}"}).text
    soup = BeautifulSoup(html,"html.parser")
    all_tags = soup.find_all(class_="date")
    for tag in all_tags:
        next = tag.find_next_sibling()
        domain = str(next["href"])
        domain = domain.replace("/","")
        if domain:
            return domain

