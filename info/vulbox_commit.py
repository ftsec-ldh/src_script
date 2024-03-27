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
               "CSRF":"csrf会造成第三者的滥用",
               "SQL注入":"攻击者未经授权可以访问数据库中的数据",
               "XSS":"反射xss通过引诱用户点击一个链接到目标网站的恶意链接来实施攻击,dom型则更具危害性，受害者正常进入页面则会遭受攻击"
               }

suggestions = {
    "CSRF":"增加referer检测和csrf_token验证",
    "SQL注入":"严格限制变量类型，比如整型变量就采用intval()函数过滤，数据库中的存储字段必须对应为int型",
    "XSS":"白名单过滤 根据白名单的标签和属性对数据进行过滤，以此来对可执行的脚本进行清除(如script标签，img标签的onerror属性等",
    "信息泄露":"设置访问该信息的权限配置，或只允许某一特定IP访问",
}

def vulbox_login(user,passwd,domain,leak_type,company_name):#检测到没有cookie再执行这一步拿cookie
    title = company_name + "页面存在" + leak_type
    s = Service("drivers/win64/chromedriver.exe")
    driver_vulbox = webdriver.Chrome(service=s)
    driver_vulbox.get("https://www.vulbox.com/account/login")
    button = WebDriverWait(driver_vulbox, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-btn.ant-btn-primary.ant-btn-block')))
    username = driver_vulbox.find_element(By.ID,"coordinated_username")
    password = driver_vulbox.find_element(By.ID, "coordinated_password")
    checkbox = driver_vulbox.find_element(By.CLASS_NAME,"ant-checkbox-input")

    checkbox.click()
    username.send_keys(user)
    password.send_keys(passwd)
    button.click()
    time.sleep(5)
    cookies = driver_vulbox.get_cookies()
    with open('cookies.txt','w+') as output:
        output.write(str(cookies))
    driver_vulbox.get("https://user.vulbox.com/management/submit/72")
    driver_vulbox.find_element(By.ID, "register_bug_title").send_keys(title)  # 漏洞标题
    time.sleep(15)

    driver_vulbox.find_element(By.XPATH, "//input[@type='radio' and @class='ant-radio-input' and @value='1']").click()#漏洞类别勾选
    driver_vulbox.find_element(By.XPATH, "//input[@type='radio' and @class='ant-radio-input' and @value='0']").click()  # 参与评定勾选
    driver_vulbox.find_element(By.ID, "register_domain").send_keys(domain)  # 厂商域名
    driver_vulbox.find_elements(By.XPATH, "//input[@type='radio' and @value='2']")[1].click()#漏洞等级
    elements = driver_vulbox.find_elements(By.XPATH, '//p[@data-we-empty-p]')  # 修复建议
    driver_vulbox.execute_script("arguments[0].innerText = arguments[1];", elements[1], suggestions[leak_type])

    elements = driver_vulbox.find_elements(By.TAG_NAME, "textarea")
    driver_vulbox.execute_script("arguments[0].value = arguments[1];", elements[0], description[leak_type])#漏洞简述
    time.sleep(2)
    driver_vulbox.execute_script("arguments[0].value = arguments[1];", elements[0],
                                 description[leak_type])  # 不知道为什么要执行两遍才可以...


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
        actions = ActionChains(driver_vulbox)  # 实例化actions类

        #######厂商名称##########
        time.sleep(2)#等待加载完毕
        element_leak_company = driver_vulbox.find_elements(By.XPATH,f"//div[@class='ant-select-selection__rendered']")[2]
        actions.send_keys_to_element(element_leak_company, company_name).pause(2).perform()
        element_choice = driver_vulbox.find_element(By.XPATH,f"//li[@class='ant-select-dropdown-menu-item']")
        actions.click(element_choice).perform()
        #######厂商名称##########

        #######漏洞类型##########
        element_leak_type = driver_vulbox.find_element(By.CLASS_NAME,"ant-cascader-picker-label")
        actions.click(element_leak_type).pause(2).perform()

        element_web_leak = driver_vulbox.find_element(By.XPATH, "//li[@title='Web漏洞']")
        actions.click(element_web_leak).pause(2).perform()

        if leak_type == "信息泄露":
            element_choice = driver_vulbox.find_element(By.XPATH, "//li[@title='信息泄露']")
            actions.click(element_choice).perform()

        if leak_type == "XSS":
            element_to_click = driver_vulbox.find_element(By.XPATH, f"//li[@title='反射型XSS']")
            actions.click(element_to_click).perform()
        #######漏洞类型##########

        leak_title = driver_vulbox.find_element(By.ID, "register_bug_title")# 漏洞标题
        actions.send_keys_to_element(leak_title,title)

        choice = driver_vulbox.find_element(By.XPATH, "//input[@type='radio' and @class='ant-radio-input']")#漏洞类别勾选
        actions.click(choice)

        choice = driver_vulbox.find_element(By.XPATH, "//input[@type='radio' and @value='0']")#参与评定勾选
        actions.click(choice)

        company_domain = driver_vulbox.find_element(By.ID, "register_domain")#厂商域名
        actions.send_keys_to_element(company_domain,domain).perform()

        choice = driver_vulbox.find_elements(By.XPATH, "//input[@type='radio' and @value='2']")[1]#漏洞等级
        actions.click(choice).perform()


        elements = driver_vulbox.find_elements(By.XPATH, "//p[@data-we-empty-p]")[1]#修复建议
        actions.send_keys_to_element(elements,suggestions[leak_type]).perform()

        elements = driver_vulbox.find_element(By.XPATH,"//textarea[@id='register_bug_paper']")#漏洞简述
        actions.send_keys_to_element(elements,description[leak_type]).perform()

        input()

    else:
        print("未检测到cookie文件，即将开始登录")
        vulbox_login("username","password",domain,leak_type,company_name)#输入你的账号和密码

