from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time,platform,vthread
from lxml import etree
from bs4 import BeautifulSoup

key_words = ["后台系统","登录"]

def check_password_input(html):
    tree = etree.HTML(html)
    input_elements = tree.xpath("//input")

    for input_elem in input_elements:
        input_type = input_elem.get("type")
        if input_type == "password":
            return True

    return False

@vthread.pool(1)
def filter_back_platform(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')#无头模式
    chrome_options.add_argument('--disable-gpu')
    system = platform.system()
    # 设置Chrome驱动路径
    if system == "Windows":
        driver_path = r'drivers\win64\chromedriver.exe'
    if system == "Linux":
        driver_path = r'drivers/linux64/chromedriver'

    # 创建Chrome驱动对象
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=chrome_options)

    if "http://" not in url and "https://" not in url:
        url = "http://" + url
    try:
        driver.get(url)
        time.sleep(10)


        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')
        content = soup.prettify()#将代码格式化再判断行数

        lines = content.splitlines()
        line_count = len(lines)

        if (any(keyword in content for keyword in key_words) and 2 < line_count < 900) or (check_password_input(content) and line_count < 900):
            print(f"{url}是后台登录系统  前端代码行数：{line_count}")
            with open("后台.txt","a+") as output_file:
                output_file.write(url + "\n")
        else:
            print(f"{url}不具备后台特征 前端代码行数：{line_count}")
    except Exception as e:
        print(f"无法访问 {url}: {e}")

    driver.quit()

