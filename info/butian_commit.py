import time,os,pyperclip,ast


description = {"信息泄露":"信息泄露可能会导致黑客进一步利用敏感信息盗取更关键的内容，甚至导致系统产生RCE漏洞",
               "逻辑漏洞":"逻辑漏洞就是指攻击者利用业务的设计缺陷，获取敏感信息或破坏业务的完整性",
               "SQL注入":"攻击者未经授权可以访问数据库中的数据",
               "XSS":"反射xss通过引诱用户点击一个链接到目标网站的恶意链接来实施攻击,dom型则更具危害性，受害者正常进入页面则会遭受攻击",
               "弱口令":"弱口令可能导致未经授权的用户获得对系统、应用程序或数据的访问权限。这可能会导致数据泄露、篡改、删除或者系统被滥用,如果用户在多个网站或服务中使用相同的弱密码，一旦其中一个网站的密码泄露，攻击者就能够使用该密码尝试登录其他网站，进而导致更大范围的信息泄露",
               "代码执行":"远程代码执行简称RCE，是一类软件安全缺陷/漏洞。RCE 漏洞将允许恶意行为人通过 LAN、WAN 或 Internet 在远程计算机上执行自己选择的任何代码，属于更广泛的任意代码执行 (ACE) 漏洞类别。"

               }

suggestions = {
    "逻辑漏洞":"修复不严谨的业务判断逻辑，对关键参数和用户COOKIE或鉴权认证进行校验",
    "SQL注入":"严格限制变量类型，比如整型变量就采用intval()函数过滤，数据库中的存储字段必须对应为int型",
    "XSS":"白名单过滤 根据白名单的标签和属性对数据进行过滤，以此来对可执行的脚本进行清除(如script标签，img标签的onerror属性等",
    "信息泄露":"设置访问该信息的权限配置，或只允许某一特定IP访问",
    "弱口令":"使用足够长度、包含大小写字母、数字和特殊字符的密码；还可以实施密码策略，要求用户设置符合安全标准的密码，如长度、复杂度要求，并对密码进行定期的过期和强制更改",
    "代码执行":"1.通用的修复方案，升级插件/框架/服务最新版\n2.如若必须使用危险函数，那么针对危险函数进行过滤\n3.在进入执行命令函数前进行严格的检测和过滤\n4.尽量不要使用命令执行函数，不能完全控制的危险函数最好不使用，如果非要用的话可以加验证防止被其他人利用"
}

def butian_login(user,passwd):#检测到没有cookie再执行这一步拿cookie
    from selenium import webdriver
    from selenium.webdriver.chrome.webdriver import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from info.api import get_company, aiqicha_get
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys

    s = Service("drivers/win64/chromedriver.exe")
    driver_butian = webdriver.Chrome(service=s)
    driver_butian.get("https://user.skyeye.qianxin.com/user/sign-in?next=https://www.butian.net/login.html?ut=1&style=1")
    button = WebDriverWait(driver_butian, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'q-button.login-btn.q-button--primary.q-button--medium')))
    username = driver_butian.find_element(By.XPATH,"//input[@class='q-input__inner' and @type='text']")
    password = driver_butian.find_element(By.XPATH,"//input[@class='q-input__inner' and @type='password']")
    checkbox = driver_butian.find_element(By.CLASS_NAME,"q-checkbox__inner")

    checkbox.click()
    username.send_keys(user)
    password.send_keys(passwd)
    button.click()
    print("请手动过验证码")
    WebDriverWait(driver_butian, 600).until(EC.presence_of_element_located((By.XPATH,'//a[@id="btnSub"]')))#等待验证码验证
    time.sleep(10)
    cookies = driver_butian.get_cookies()
    with open('butian_cookies.txt','w+') as output:
        output.write(str(cookies))
    driver_butian.quit()
    print("请重新执行该软件")

def butian_src_page(domain,leak_type,leak_url):
    from selenium import webdriver
    from selenium.webdriver.chrome.webdriver import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from info.api import get_company, aiqicha_get
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys

    if os.path.exists("butian_cookies.txt"):
        company_name = get_company(domain, 1)#获取公司名
        area_dict = aiqicha_get(company_name, 1)#获取公司地址、注册资金、行业划分
        title = company_name + "页面存在" + leak_type

        s = Service("drivers/win64/chromedriver.exe")
        driver_butian = webdriver.Chrome(service=s)

        driver_butian.get("https://www.butian.net")
        with open("butian_cookies.txt", "r+") as cookie_input:
            cookies = ast.literal_eval(cookie_input.read())
        for cookie in cookies:
            driver_butian.add_cookie(cookie)
        driver_butian.get("https://www.butian.net/Loo/submit")

        actions = ActionChains(driver_butian)  # 实例化actions类

        time.sleep(1)#等待1秒

        element = driver_butian.find_element(By.XPATH, f"//input[@name='company_name']")#厂商名称
        actions.send_keys_to_element(element, company_name).pause(0.5).perform()

        element = driver_butian.find_element(By.XPATH, f"//input[@placeholder='输入所属域名或ip，若存在多个以,分隔']")#域名或ip
        actions.send_keys_to_element(element, domain).pause(0.5).perform()

        element = driver_butian.find_element(By.XPATH, f"//input[@placeholder='单位名称+漏洞类型，如：某单位存在SQL注入漏洞']")#漏洞标题
        actions.send_keys_to_element(element, title).pause(0.5).perform()

        element = driver_butian.find_element(By.XPATH, f"//input[@placeholder='URL格式：以http://或https://开头']")#漏洞URL
        actions.send_keys_to_element(element, leak_url).pause(0.5).perform()


        s1 = Select(driver_butian.find_element(By.ID, "lootypesel2"))#漏洞类型
        s1.select_by_visible_text(leak_type)

        s1 = Select(driver_butian.find_element(By.ID, "level"))#漏洞等级
        s1.select_by_visible_text("中危")

        element = driver_butian.find_element(By.XPATH, f"//textarea[@id='description']")#漏洞简述
        actions.send_keys_to_element(element, description[leak_type]).pause(1).perform()

        element = driver_butian.find_element(By.XPATH, f"//textarea[@id='repair_suggest']")#修复方案
        actions.send_keys_to_element(element, suggestions[leak_type]).pause(1).perform()

        print(area_dict)

        dict_change = {
            "科技推广和应用服务业":"科学研究和技术服务业",
            "软件和信息技术服务业":"信息传输、软件和信息技术服务业",
            "文化艺术业":"文化、体育和娱乐业",
            "电气机械和器材制造业":"制造业",
            "互联网和相关服务":"信息传输、软件和信息技术服务业",
            "专业技术服务业":"信息传输、软件和信息技术服务业",
            "商务服务业":"租赁和商务服务业",
            "批发业":"批发和零售业",
            "零售业":"批发和零售业"}
        try:
            s1 = Select(driver_butian.find_element(By.ID, "industry1"))#所属行业
            s1.select_by_visible_text(dict_change[area_dict["division"]])
        except Exception:
            print("该域名所属行业未知，如爱企查显示有行业则说明配置丢失")

        division_type = {
            '电信、广播电视和卫星传输服务': "30",
            "文化艺术业": "78",
            "电气机械和器材制造业": "85",
            "批发业":"95",
            "零售业":"96",
            '商务服务业':"279",
            '软件和信息技术服务业': "330",
            '互联网和相关服务': "331",
            "专业技术服务业":"331",
            '科技推广和应用服务业':"335",
        }
        try:#行业分类checkbox
            element = WebDriverWait(driver_butian, 10).until(EC.presence_of_element_located((By.XPATH, f"//input[@id='{division_type[area_dict['division']]}']")))
            actions.click(element).perform()
        except Exception:
            print("该域名所属行业未知，如爱企查显示有行业则说明配置丢失")

        select_elements = driver_butian.find_elements(By.ID, "selec1")#所属地区-省
        for select in select_elements:
            dropdown = Select(select)
            options = dropdown.options
            for option in options:
                if area_dict['province'] in option.text:
                    dropdown.select_by_visible_text(option.text)
                    break

        special = ['北京','上海','重庆','天津']
        if area_dict["province"] not in special:#四个特殊地区单独选择
            select_elements = driver_butian.find_elements(By.ID, "selec2")#所属地区-市
            for select in select_elements:
                dropdown = Select(select)
                options = dropdown.options
                for option in options:
                    if area_dict['city'] in option.text:
                        dropdown.select_by_visible_text(option.text)
                        break

            select_elements = driver_butian.find_elements(By.ID, "selec3")#所属地区-区
            for select in select_elements:
                dropdown = Select(select)
                options = dropdown.options
                for option in options:
                    try:
                        if area_dict['area'] in option.text:
                            dropdown.select_by_visible_text(option.text)
                            break
                    except Exception:
                        print("该域名所属地区未知，如爱企查显示有行业则说明配置丢失")

        else:#四个地区在里面就这样选
            s1 = Select(driver_butian.find_element(By.ID, "selec2"))#所属地区-4个特殊城市+城区
            s1.select_by_index(1)

            select_elements = driver_butian.find_elements(By.ID, "selec3")#所属地区-区
            for select in select_elements:
                dropdown = Select(select)
                options = dropdown.options
                for option in options:
                    if area_dict['city'] in option.text:
                        dropdown.select_by_visible_text(option.text)
                        break
        try:
            element = driver_butian.find_element(By.XPATH, f"//input[@placeholder='厂商联系方式']")  # 厂商联系方式
            actions.send_keys_to_element(element, area_dict['phone_number']).pause(1).perform()
        except Exception:
            print("查询电话出错，可能该公司较特殊，请手动查询该公司电话")



        input()
    else:
        print("未检测到cookie文件，请手动登录")
        username = input("请输入你的账号：")
        password = input("请输入你的密码：")
        butian_login(username,password)

