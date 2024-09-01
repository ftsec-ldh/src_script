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
api_url3 = "https://aiqicha.baidu.com/s?q="  # 查公司注册资金的接口

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
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        # prefs = {
        #     "profile.managed_default_content_settings.images": 2,
        #     "profile.default_content_setting_values": {
        #         "automatic_downloads": 1,
        #         "notifications": 1,
        #         "popups": 1,
        #         "geolocation": 1
        #     }
        # }
        # chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument("--disable-blink-features")
        # chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument('disable-infobars')
        # # 禁用安全警告
        # chrome_options.add_argument('--disable-web-security')
        # chrome_options.add_argument("--ignore-certificate-errors")
        # chrome_options.add_argument("--allow-running-insecure-content")
        # # 禁止自动跳转(http自动跳转成https)
        # chrome_options.add_argument("--disable-features=AutomaticHttpsRedirect")

    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")

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
    url = get_main(url)
    url = api_url + url
    driver = create_driver()

    driver.get(url)
    time.sleep(2)
    text = driver.page_source
    name = re.findall(r"<span id=\"icp_company\">(.*?)</span></li>",text)
    name = ''.join(name)
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

def aiqicha_get(company_name,picture=0):#返回字典[公司省份、区市、注册资金、行业划分，联系电话]
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    aiqicha_driver = create_driver(0)
    if os.path.exists("aiqicha_cookies.txt"):
        aiqicha_driver.get(f"https://aiqicha.baidu.com/")
        with open("aiqicha_cookies.txt", "r+") as cookie_input:
            try:
                cookies = ast.literal_eval(cookie_input.read())
            except SyntaxError:
                print("aiqicha_cookie格式有误，请删除该文件重新获取cookie")
        for cookie in cookies:
            try:
                aiqicha_driver.add_cookie(cookie)
            except Exception:
                pass
        print(f"公司名：{company_name}")
        aiqicha_driver.get(f"https://aiqicha.baidu.com/s?q={company_name}&t=0")
        try:
            WebDriverWait(aiqicha_driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='wrap']/a"))
            )  # 等待元素
        except Exception:
            os.remove("aiqicha_cookies.txt")
            print("检测到需要重新过验证码，已自动删除aiqicha_cookies.txt，请重启我再次更新cookies，")
            exit()

        html = aiqicha_driver.page_source

        if picture == 1:
            aiqicha_driver.get_screenshot_as_file(f"aiqicha_{company_name}.png")#截图

        html_tree = etree.HTML(html)
        elements = html_tree.xpath("//div[@class='wrap']/a")[0].get("data-log-title")#获取第一个超链接跳转地址
        detail_page = "/company_detail_" + str(re.findall(r"\d.+",elements)[0])
        aiqicha_driver.get(f"https://aiqicha.baidu.com/{detail_page}")#使用无头模式这里会被检测到

        WebDriverWait(aiqicha_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//td[preceding-sibling::td[@data-v-3869a30a='' and contains(text(), '行政区划')]]"))
        )#等待元素

        html = aiqicha_driver.page_source


        html_tree = etree.HTML(html)

        elements = html_tree.xpath("//td[preceding-sibling::td[@data-v-3869a30a='' and contains(text(), '行政区划')]]")
        address = elements[0].text


        elements = html_tree.xpath("//td[preceding-sibling::td[contains(text(),'所属行业')]]")
        division = elements[0].text.replace("\n","").replace(" ","")
        if division == "-":
            division = "None"

        try:
            elements = html_tree.xpath("//td[contains(text(), '元')]")
            money = elements[0].text.replace(" ","").replace("\n","").replace("(元)","")
        except Exception:
            money = "None"
        try:
            elements = html_tree.xpath('//span[@data-log-an="detail-head-phone"]/span')
            phone_number = elements[0].text
        except Exception:
            phone_number = None

        if phone_number == None:#有些网站的手机号码是div包裹的
            elements = html_tree.xpath('//div[@class="ivu-poptip-rel"]')
            for i in range(len(elements)):
                if elements[i] is not None and hasattr(elements[i], 'text'):
                    phone_number = elements[i].text
                    if phone_number is not None and not bool(re.search(r'[\u4e00-\u9fff]', phone_number)):
                        phone_number = phone_number.replace(".", "").replace(" ", "").strip()
                        break
        print(address)

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
            city = re.findall(r"省(.+)市",address)[0]
            area = extract_district(address)

        aiqicha_driver.quit()
        return {"money":money,"province":province,"city":city,"area":area,"division":division,"phone_number":phone_number}

    else:
        print("检测到你没有过验证，请手动过验证：")
        aiqicha_captcha()

def aiqicha_captcha():
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    aiqicha_driver = create_driver(0)
    aiqicha_driver.get(f"https://aiqicha.baidu.com/")
    time.sleep(3)
    aiqicha_driver.delete_all_cookies()
    aiqicha_driver.get(f"https://aiqicha.baidu.com/")

    WebDriverWait(aiqicha_driver, 600).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='search-btn']"))
    )  # 等待元素

    input("如需获取电话号码，请登录爱企查，登陆完毕输入任意字符继续：")

    cookies = aiqicha_driver.get_cookies()
    with open("aiqicha_cookies.txt", "w+") as output:
        output.write(str(cookies))
    aiqicha_driver.quit()
    print("写入cookie完成，请重启我")
    exit()
