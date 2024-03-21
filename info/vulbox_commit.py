from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from info.api import get_company
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time,os

description = {"信息泄露":"信息泄露可能会导致黑客进一步利用敏感信息盗取更关键的内容，甚至导致系统产生RCE漏洞",
               "csrf":"csrf会造成第三者的滥用"}

suggestions = {
    "csrf":"增加referer检测和csrf_token验证",
    "sql注入":"严格限制变量类型，比如整型变量就采用intval()函数过滤，数据库中的存储字段必须对应为int型",
    "xss":"白名单过滤 根据白名单的标签和属性对数据进行过滤，以此来对可执行的脚本进行清除(如script标签，img标签的onerror属性等",
    "信息泄露":"设置访问该信息的权限配置，或只允许某一特定IP访问",
}

def vulbox_login(user,passwd):#检测到没有cookie再执行这一步拿cookie

    s = Service("drivers/win64/chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get("https://www.vulbox.com/account/login")
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-btn.ant-btn-primary.ant-btn-block')))
    username = driver.find_element(By.ID,"coordinated_username")
    password = driver.find_element(By.ID, "coordinated_password")
    checkbox = driver.find_element(By.CLASS_NAME,"ant-checkbox-input")

    checkbox.click()
    username.send_keys(user)
    password.send_keys(passwd)
    button.click()
    time.sleep(5)
    cookies = driver.get_cookies()
    driver.get("https://user.vulbox.com/management/submit/72")
    with open('cookies.txt','w+') as output:
        output.write(str(cookies))
    input()

def vulbox_src_page(domain,leak_type):
    company_name = get_company(domain)
    title = company_name + "页面存在" + leak_type

    if os.path.exists("cookies.txt"):
        s = Service("drivers/win64/chromedriver.exe")
        driver_vulbox = webdriver.Chrome(service=s)
        driver_vulbox.get("https://www.vulbox.com/account/login")

        with open("cookies.txt", "r+") as cookie_input:
            cookies = eval(cookie_input.read())
        for cookie in cookies:
            driver_vulbox.add_cookie(cookie)

        driver_vulbox.get("https://user.vulbox.com/management/submit/72")
        driver_vulbox.find_element(By.ID, "register_bug_title").send_keys(title)  # 漏洞标题
        time.sleep(15)

        driver_vulbox.find_element(By.XPATH, "//input[@type='radio' and @value='0']").click()#返回参与评定勾选的对象
        driver_vulbox.find_element(By.ID, "register_domain").send_keys(domain)#厂商域名
        driver_vulbox.find_elements(By.XPATH, "//input[@type='radio' and @value='2']")[1].click()#漏洞等级

        elements = driver_vulbox.find_elements(By.XPATH, '//p[@data-we-empty-p]')#修复建议
        driver_vulbox.execute_script("arguments[0].innerText = arguments[1];", elements[1], suggestions[leak_type])

        elements = driver_vulbox.find_elements(By.TAG_NAME,"textarea")
        driver_vulbox.execute_script("arguments[0].value = arguments[1];",elements[0],description[leak_type])#漏洞简述
        time.sleep(1)
        driver_vulbox.execute_script("arguments[0].value = arguments[1];", elements[0],description[leak_type])#不知道为什么要执行两遍才可以...

        input()

    else:
        print("未检测到cookie文件，即将开始登录")
        vulbox_login("1607131160","xin4680241")

