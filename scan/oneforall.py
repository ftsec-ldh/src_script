import os
import ast
import pandas as pd
from pandas.errors import EmptyDataError
import glob
import subprocess,time
import numpy as np



def domain_scan(domain_search):# oneforall联动subfinder
    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)

    oneforall_path = config['oneforall_path']
    subfinder_path = config['subfinder_path']

    urls = set()

    command = ['python', f'{oneforall_path}/oneforall.py', '--valid=None', '--verify=False',f'--target={domain_search}', 'run']
    print(f"正在调用OneForAll收集域名：{domain_search}，请耐心等待！")
    try:
        subprocess.run(command, capture_output=True, text=True,encoding='utf-8')
    except Exception as e:
        print(f"输出：{e}")

    try:
        df = pd.read_csv(f"{oneforall_path}/results/{domain_search}.csv", encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(f"{oneforall_path}/results/{domain_search}.csv", encoding='latin1')
    except EmptyDataError:
        print(f"OneForAll查询域名：{domain_search}的结果为空")

    try:
        valid_urls = df['subdomain'].tolist()
        for url in valid_urls:
            urls.add(url)
    except Exception:
        pass

    command = [f'{subfinder_path}/subfinder.exe', '-d', domain_search]
    print(f"正在调用SubFinder收集域名：{domain_search}，请耐心等待！")
    result = subprocess.run(command, capture_output=True, text=True,encoding='utf-8')

    if result.stdout:#检查输出是否存在
        for url in result.stdout.split("\n"):
            if url:#确保url不为空
                urls.add(url)

    # 删除nan类型的float元素
    urls.discard(np.nan)
    urls.discard('')
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    s = Service("drivers/win64/chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver_search_domain = webdriver.Chrome(service=s,options=chrome_options)

    driver_search_domain.get(f"https://www.virustotal.com/gui/domain/{domain_search}/relations")

    time.sleep(3)

    captcha_frame = driver_search_domain.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
    driver_search_domain.switch_to.frame(captcha_frame)

    try:#不报错说明要验证
        captcha_element = driver_search_domain.find_element(By.XPATH, "//label[@id='recaptcha-anchor-label']")
        print("检测到需要过验证")
    except Exception:
        print("无需过验证码")
        #检测是否存在(更多)按钮
        driver_search_domain.switch_to.default_content()
        element = WebDriverWait(driver_search_domain, 600).until(EC.presence_of_element_located((By.XPATH, "//domain-view[@name='domain-view']")))
        shadow_root1 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

        element = shadow_root1.find_element(By.CSS_SELECTOR, "vt-ui-domain-relations#relations")
        shadow_root2 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

        element = shadow_root2.find_element(By.CSS_SELECTOR, "vt-ui-expandable[class=' mb-3 subdomains ']")

        element = element.find_element(By.CSS_SELECTOR, "vt-ui-button[class='load-more mt-3']")
        shadow_root3 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

        button = shadow_root3.find_element(By.CSS_SELECTOR, "div.spinner")
        driver_search_domain.execute_script("arguments[0].click();", button)
        if element.get_attribute('hidden') == None:#没有隐藏，继续点，直到hidden为true
            print("检测到域名有很多，还需要继续获取")
            for i in range(999):#循环获取域名
                element = WebDriverWait(driver_search_domain, 600).until(EC.presence_of_element_located((By.XPATH, "//domain-view[@name='domain-view']")))
                shadow_root1 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

                element = shadow_root1.find_element(By.CSS_SELECTOR, "vt-ui-domain-relations#relations")
                shadow_root2 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

                element = shadow_root2.find_element(By.CSS_SELECTOR, "vt-ui-expandable[class=' mb-3 subdomains ']")

                element = element.find_element(By.CSS_SELECTOR,"vt-ui-button[class='load-more mt-3']")
                shadow_root3 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

                button = shadow_root3.find_element(By.CSS_SELECTOR, "div.spinner")
                driver_search_domain.execute_script("arguments[0].click();", button)
                time.sleep(0.5)
                if element.get_attribute('hidden'):#按钮消失说明域名取完了
                    print("域名好像不需要获取了，可以了")
                    break
        else:
            print("域名好像不需要获取了，可以了")

        element = WebDriverWait(driver_search_domain, 600).until(EC.presence_of_element_located((By.XPATH, "//domain-view[@name='domain-view']")))
        shadow_root1 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

        element = shadow_root1.find_element(By.CSS_SELECTOR, "vt-ui-domain-relations#relations")
        shadow_root2 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)#vt-ui-generic-list

        element = shadow_root2.find_element(By.CSS_SELECTOR, "vt-ui-generic-list")
        shadow_root3 = driver_search_domain.execute_script('return arguments[0].shadowRoot', element)

        tag_a_elements = shadow_root3.find_elements(By.CSS_SELECTOR,"a[class='styled-link']")
        for tag_a_element in tag_a_elements:
            if domain_search in tag_a_element.text:
                urls.add(tag_a_element.text)

        return urls

