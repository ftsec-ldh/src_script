import time,os,pyperclip,ast


description = {"信息泄露":"信息泄露可能会导致黑客进一步利用敏感信息盗取更关键的内容，甚至导致系统产生RCE漏洞",
               "CSRF":"csrf会造成第三者的滥用",
               "SQL注入":"攻击者未经授权可以访问数据库中的数据",
               "XSS":"反射xss通过引诱用户点击一个链接到目标网站的恶意链接来实施攻击,dom型则更具危害性，受害者正常进入页面则会遭受攻击",
               "弱口令":"弱口令可能导致未经授权的用户获得对系统、应用程序或数据的访问权限。这可能会导致数据泄露、篡改、删除或者系统被滥用,如果用户在多个网站或服务中使用相同的弱密码，一旦其中一个网站的密码泄露，攻击者就能够使用该密码尝试登录其他网站，进而导致更大范围的信息泄露"
               }

suggestions = {
    "CSRF":"增加referer检测和csrf_token验证",
    "SQL注入":"严格限制变量类型，比如整型变量就采用intval()函数过滤，数据库中的存储字段必须对应为int型",
    "XSS":"白名单过滤 根据白名单的标签和属性对数据进行过滤，以此来对可执行的脚本进行清除(如script标签，img标签的onerror属性等",
    "信息泄露":"设置访问该信息的权限配置，或只允许某一特定IP访问",
    "弱口令":"使用足够长度、包含大小写字母、数字和特殊字符的密码；还可以实施密码策略，要求用户设置符合安全标准的密码，如长度、复杂度要求，并对密码进行定期的过期和强制更改"
}

def vulbox_login(user,passwd):#检测到没有cookie再执行这一步拿cookie
    from selenium import webdriver
    from selenium.webdriver.chrome.webdriver import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

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
    with open('vulbox_cookies.txt','w+') as output:
        output.write(str(cookies))
    driver_vulbox.quit()
    print("请重新执行该软件")

def vulbox_src_page(domain,leak_type,leak_url):
    from selenium import webdriver
    from selenium.webdriver.chrome.webdriver import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from info.api import get_company, qcc_get
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys

    if os.path.exists("vulbox_cookies.txt"):
        company_name = get_company(domain,1)#获取公司名
        area_dict = qcc_get(company_name,1)#获取公司地址、注册资金、行业划分,1代表要拍照
        title = company_name + "页面存在" + leak_type

        s = Service("drivers/win64/chromedriver.exe")
        driver_vulbox = webdriver.Chrome(service=s)
        driver_vulbox.get("https://www.vulbox.com/account/login")
        with open("vulbox_cookies.txt", "r+") as cookie_input:
            cookies = ast.literal_eval(cookie_input.read())
        for cookie in cookies:
            driver_vulbox.add_cookie(cookie)

        driver_vulbox.get("https://user.vulbox.com/management/submit/72")
        actions = ActionChains(driver_vulbox)  # 实例化actions类

        time.sleep(3)

        #######厂商名称##########
        element_leak_company = driver_vulbox.find_elements(By.XPATH,f"//div[@class='ant-select-selection__rendered']")[2]
        actions.send_keys_to_element(element_leak_company, company_name).pause(2).perform()
        element_choice = driver_vulbox.find_element(By.XPATH,f"//li[@class='ant-select-dropdown-menu-item']")
        actions.click(element_choice).perform()
        #######厂商名称##########

        #######漏洞类型##########
        element_leak_type = driver_vulbox.find_element(By.CLASS_NAME,"ant-cascader-picker-label")
        actions.click(element_leak_type).perform()

        WebDriverWait(driver_vulbox, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[@title='Web漏洞']"))
        )#等待元素

        element_web_leak = driver_vulbox.find_element(By.XPATH, "//li[@title='Web漏洞']")
        actions.click(element_web_leak).perform()

        WebDriverWait(driver_vulbox, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//li[@title='{leak_type}']"))
        )#等待元素

        element_choice = driver_vulbox.find_element(By.XPATH, f"//li[@title='{leak_type}']")
        actions.click(element_choice).perform()


        #######漏洞类型##########

        leak_title = driver_vulbox.find_element(By.ID, "register_bug_title")# 漏洞标题
        actions.send_keys_to_element(leak_title,title)

        choice = driver_vulbox.find_element(By.XPATH, "//input[@type='radio' and @class='ant-radio-input']")#漏洞类别勾选
        actions.click(choice)

        choice = driver_vulbox.find_element(By.XPATH, "//input[@type='radio' and @value='0']")#参与评定勾选
        actions.click(choice)

        choice = driver_vulbox.find_elements(By.XPATH, "//input[@type='radio' and @value='2']")[1]  # 漏洞等级-中危
        actions.click(choice).perform()

        company_domain = driver_vulbox.find_element(By.ID, "register_domain")#厂商域名
        actions.send_keys_to_element(company_domain,domain).perform()

        elements = driver_vulbox.find_elements(By.XPATH, "//p[@data-we-empty-p]")[1]#修复建议
        actions.send_keys_to_element(elements,suggestions[leak_type]).perform()

        elements = driver_vulbox.find_element(By.XPATH,"//textarea[@id='register_bug_paper']")#漏洞简述
        actions.move_to_element(elements).send_keys(Keys.PAGE_UP).perform()#往上滚动防止点不到漏洞简述
        actions.send_keys_to_element(elements,description[leak_type]).perform()


        elements = driver_vulbox.find_element(By.XPATH,"//input[@placeholder='请输入漏洞url或出现的功能点']")#漏洞URL/功能点
        actions.send_keys_to_element(elements,leak_url).perform()

        province = area_dict["province"]

        element = driver_vulbox.find_element(By.XPATH,"//input[@placeholder='请选择所属地区']")
        actions.click(element).perform()

        WebDriverWait(driver_vulbox, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[@title]"))
        )#等待元素

        special = ['北京','天津','上海','重庆']
        if province in special and "重庆" not in province:
            element = driver_vulbox.find_element(By.XPATH,f"//li[@title='{province}']")
            actions.click(element).perform()

            city = province + "市"

            WebDriverWait(driver_vulbox, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//li[@title='{city}']"))
            )  # 等待元素

            element = driver_vulbox.find_element(By.XPATH,f"//li[@title='{city}']")
            actions.click(element).perform()
        elif "重庆" in province:
            element = driver_vulbox.find_element(By.XPATH,f"//li[@title='{province}']")
            actions.click(element).perform()#重庆没有city
        else:
            city = area_dict["city"]
            element = driver_vulbox.find_element(By.XPATH, f"//li[@title='{province}']")
            actions.click(element).perform()

            WebDriverWait(driver_vulbox, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//li[contains(text(),'{city}')]"))
            )  # 等待元素

            element = driver_vulbox.find_element(By.XPATH,f"//li[contains(text(),'{city}')]")
            actions.click(element).perform()

        input()

    else:
        print("未检测到cookie文件，请手动登录")
        username = input("请输入你的账号：")
        password = input("请输入你的密码：")
        vulbox_login(username,password)

