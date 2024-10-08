#从IP或域名列表中快速提取关键部分
import platform,time,socket,urllib3,requests,re,random


from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import os,base64,ast
from lxml import etree
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.72 Safari/537.36'}

api_url = "https://www.aizhan.com/cha/"  # 查权重的接口
api_url2 = "http://site.ip138.com/"  # 反查域名的接口
api_url3 = "https://www.qcc.com/"  # 查公司注册资金的接口

def create_driver(无头模式=1):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service

    system = platform.system()
    if system == "Windows":
        driver_path = r'drivers\win64\chromedriver.exe'
    if system == "Linux":
        driver_path = r'drivers/linux64/chromedriver'
    if system == "Darwin":
        driver_path = r'drivers/mac64/chromedriver'

    chrome_options = webdriver.ChromeOptions()

    if 无头模式 == 1:
        chrome_options.add_argument("--headless")

    chrome_options.page_load_strategy = 'none'
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    s = Service(driver_path)

    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver

#将提取到的域名取主域名
def extract_main_domain(line):
    def get_main_domain(domain):
        # 移除域名中的端口号（如果有）
        domain = domain.split(':')[0]
        parts = domain.split('.')
        if len(parts) < 2:
            return domain
        if parts[-1] in ('cn', 'com', 'net', 'org', 'gov', 'edu'):
            return '.'.join(parts[-3:]) if parts[-2] in ('com', 'net', 'org', 'gov', 'edu') else '.'.join(parts[-2:])
        else:
            return '.'.join(parts[-2:])

    if line.startswith('ip：'):
        domain_match = re.search(r'域名：([a-zA-Z0-9.-]+)', line)
        if domain_match:
            domain = domain_match.group(1)
            return get_main_domain(domain)
    elif line.startswith('站点：'):
        site_match = re.search(r'站点：https?://([a-zA-Z0-9.-]+)', line)
        if site_match:
            site = site_match.group(1)
            return get_main_domain(site)
        else:
            domain_match = re.search(r'站点：([a-zA-Z0-9.-]+)', line)
            if domain_match:
                domain = domain_match.group(1)
                return get_main_domain(domain)
    else:
        # 如果不是以ip或站点开头，直接处理整个行为一个域名
        return get_main_domain(line.strip())

    return None



def get_ip_address(domain):#ping功能，反查域名再正向解析判断域名是否真的绑定了IP
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "Error: Unable to resolve domain"

#获取单位名称
def get_company(url,picture=1):#picture等于1则截图
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    url = get_main(url)
    url = api_url + url
    driver = create_driver(0)

    driver.get(url)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='icp_company']")))
    name = element.text
    if "（" in name:
        kuohao_index = name.index("（")
        name = name[:kuohao_index]
    if picture == 1:
        driver.get_screenshot_as_file(f"aizhan_{name}.png")
    print(name)
    return name

#获取权重
def get_rank(url):
    url = get_main(url)
    url = api_url + url
    driver = create_driver()

    driver.get(url)
    text = driver.page_source

    rank_bd = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/br/(.*?).png", text))
    rank_yd = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/mbr/(.*?).png", text))
    rank_360 = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/360/(.*?).png", text))
    rank_sm = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/sm/(.*?).png", text))
    rank_sg = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/sr/(.*?).png", text))
    rank_gg = "".join(re.findall(r"<img src=\"//statics.aizhan.com/images/pr/(.*?).png", text))

    return rank_bd,rank_yd,rank_360,rank_sm,rank_sg,rank_gg


def get_main(url):
    if "http://" not in url and "https://" not in url:
        url = "http://" + url
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    ip_match = re.search(ip_pattern, url)
    if ip_match:#说明是ip
        main_part = ip_match.group()
    else:
        domain_pattern = r"https?://([^:/]+)"#提取域名
        domain_match = re.findall(domain_pattern, url)
        if domain_match:
            main_part = domain_match[0]
        else:
            main_part = ""
    return main_part


def base64_encode(data):
    byte_data = data.encode('utf-8')
    encoded_data = base64.b64encode(byte_data)
    return encoded_data.decode('utf-8')


def get_domain_byIP(line,fofa=0,proxies=0):
    time.sleep(4)#防拉黑
    ip = get_main(line)
    if fofa == 1:#爬fofa
        base64 = base64_encode(f'ip="{ip}" && is_domain=true')
        text = requests.get(f"https://fofa.info/result?qbase64={base64}",headers=headers).text
        html_etree = etree.HTML(text)
        elements = html_etree.xpath("//span[@class='hsxa-highlight-color']")
        total_result = elements[0].text
        if total_result == '0':
            return False
        else:
            domains = html_etree.xpath("//span[@class='hsxa-host']/a")
            domain = domains[0].text.replace(" ","").replace("\n","")
            return domain
    else:#爬ip138
        proxy = random.choice(proxies)
        url = api_url2 + ip

        try:
            html = requests.get(url,headers=headers,proxies={"http":f"http://{proxy}"},timeout=10).text
        except Exception:
            return f"error：{proxy}"

        if "暂无结果" in html:
            return False

        soup = BeautifulSoup(html,"html.parser")
        all_tags = soup.find_all(class_="date")
        for tag in all_tags:
            next = tag.find_next_sibling()
            domain = str(next["href"])
            domain = domain.replace("/","")
            if domain:
                return domain

def crawl_company(line,fofa=0,proxies=0,again=0):#fofa=0不启用fofa | proxies为0反查不用代理 | again=0写文件改个名(主域名查权重)
    ###################传参IP才执行该步骤##########################
    if re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", line):  # 检测到IP自动反查域名
        domain = get_domain_byIP(line,fofa,proxies)#无结果返回false，代理池出错返回error 0代表用ip138
        if domain and "error" not in domain:#找到了域名且代理池不出错
            name = get_company(domain)
            rank = get_rank(domain)
            content = f"ip：{line}，域名：{domain},公司名：{name}, 权重：{rank}"
            print(content, end="\n")
            if "-" not in name and len(name) != 0:
                with open("公司权重.txt", "a+") as output:
                    output.write(content + "\n")

        if domain == False:#无结果
            print(line.replace("http://", "").replace("https://", "") + "未绑定域名，跳过此次查询", end="\n")

        if "error" in str(domain):#代理池出错
            return f"{str(domain)}"#返回代理池错误信息

    ###################传参IP才执行该步骤##########################
    ###################传参域名才执行该步骤##########################
    else:
        name = get_company(line)
        content = f"站点：{line},公司名：{name}, 权重：{get_rank(line)}"
        print(content, end="\n")
        if "-" not in name and len(name) != 0:
            if again == 0:
                with open("公司权重.txt", "a+") as output:
                    output.write(content + "\n")
            if again == 1:
                with open("主域名查权重.txt", "a+") as output2:
                    output2.write(content + "\n")
    ###################传参域名才执行该步骤##########################

def extract_district(text):#提取区
    pattern = r'([\u4e00-\u9fa5]+省)?([\u4e00-\u9fa5]+市)([\u4e00-\u9fa5]+区|市)'
    match = re.search(pattern, text)
    if match:
        district = match.group(3)
        return district
    else:
        return None

def qcc_get(company_name,picture=0):#返回字典[公司省份、区市、注册资金、行业划分，联系电话]
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    qcc_driver = create_driver(1)

    qcc_driver.get("https://www.qcc.com")
    if not os.path.exists("qcc_cookies.txt"):
        print("检测到企查查cookies文件不存在，请你手动登录企查查")
        qcc_login()


    qcc_driver.get("https://www.qcc.com")
    time.sleep(6)
    qcc_driver.delete_all_cookies()


    with open("qcc_cookies.txt","r") as f:
        cookies = ast.literal_eval(f.read())
    for cookie in cookies:
        qcc_driver.add_cookie(cookie)

    qcc_driver.get("https://www.qcc.com")

    try:
        WebDriverWait(qcc_driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[text()='登录 | 注册']")))
        print("检测到cookie失效，请手动删除cookie文件重新登录")
        qcc_login()
    except Exception:

        element = WebDriverWait(qcc_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='searchKey']")))
        element.send_keys(company_name)

        element = WebDriverWait(qcc_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary']")))
        element.click()

        element = WebDriverWait(qcc_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='title copy-value']")))
        url = element.get_attribute("href")

        if picture == 1:
            qcc_driver.get_screenshot_as_file(f"qcc_{company_name}.png")#截图

        qcc_driver.get(url)

        WebDriverWait(qcc_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(),'国标行业')]")))
        html = qcc_driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        td_element = soup.find('td', text='所属地区')
        next_td = td_element.find_next_sibling('td')
        span_element = next_td.find('span', class_='copy-value')
        address = span_element.text#公司地址

        parser = etree.HTMLParser()
        tree = etree.fromstring(html, parser)

        td_element = tree.xpath("//td[contains(text(), '国标行业')]/following-sibling::td[1]")
        span_element = td_element[0].xpath(".//span[not(@class)]")
        division = span_element[0].text#国标行业

        td_element = tree.xpath("//td[span[contains(text(), '注册资本')]]/following-sibling::td[1]")
        money = td_element[0].text#注册资本

        span_element = tree.xpath("//span[@class='f overhide-part']/span[text()='电话：']")
        phone_span = span_element[0].xpath(".//following-sibling::span//span[@class='copy-value']")#电话
        try:
            phone_number = phone_span[0].text
        except Exception:
            print("未寻找到电话号码，可能电话需要VIP")
            phone_number = None

        if "北京" in address or "重庆" in address or "上海" in address or "天津" in address:
            province = re.findall(r"(.+)市",address)[0]
            try:
                city = re.findall(r"市(.+)",address)[0]
            except Exception:
                city = None
            area = "None"
        elif "西藏自治区" in address:
            province = "西藏"
            city = re.findall(r"区(.+)",address)[0]
            area = "None"
        elif "新疆维吾尔自治区" in address:
            province = "新疆"
            city = re.findall(r"区(.+)", address)[0]
            area = "None"
        else:
            province = re.findall(r"(.+)省",address)[0]
            try:
                city = re.findall(r"省(.+)市",address)[0]
            except Exception:
                city = None
            area = extract_district(address)

        qcc_driver.quit()
        return {"money":money,"province":province,"city":city,"area":area,"division":division,"phone_number":phone_number}

def qcc_login():
    qcc_driver = create_driver(0)
    qcc_driver.get("https://www.qcc.com/")
    input("请手动登录后输入任意值：")

    cookies = qcc_driver.get_cookies()
    with open("qcc_cookies.txt", "w+") as output:
        output.write(str(cookies))
    qcc_driver.quit()
    print("写入cookie完成，请重启我")
    exit()
