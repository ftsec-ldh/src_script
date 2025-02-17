import re,time,ast
from info.api import get_main
from info.google import google_search
from info.update_proxies import update_proxy_Bypool,update_proxy_ByFile
from info.vulbox_commit import vulbox_src_page
from info.butian_commit import butian_src_page
from filter.socket_getIP import domain_to_ip,thread_domain_to_ip
from filter.cls_repeat_ip import remove_same_ip,extract_unique_domains_ips
from filter.check_alive import filter_urls
from filter.filter_web_BackPlatform import filter_back_platform
from filter.filter_c import filter
from scan.xray_scan_urls import scan_urls,scan_urls_cookies,start_xray_listen

with open("conf/config.conf", encoding="utf-8") as config_file:
    config = config_file.read()
    config = ast.literal_eval(config)
    xray_path = config['xray_path']
    crawlergo_path = config['crawlergo_path']

if __name__ == "__main__":
    while True:
        opear = input("(1)爬取谷歌内容\n(2)批量操作\n(3)更新代理池\n(4)盒子半自动化提交\n(5)补天半自动化提交\n(6)xray一键扫描\n(7)C段汇总\n(8)cnvd半自动化提交\n请选择操作数：")
        
        if opear == "1":#爬谷歌url
            google_search()

        if opear == "2":
            print("------------------------------------------")
            choice = input('''(1)批量域名取IP地址\n(2)批量检测存活\n(3)批量提取xray结果目标\n(4)解析排除重复IP\n(5)批量提取后台系统\n(6)域名排重：''')

            if choice == "1":#批量域名取IP
                input_file = input("请输入文件名：")
                remain_domain = input("是否保留域名(y/n)：")
                thread_choice = input("是否多线程(y/n)：")
                if thread_choice == "n":
                    output_file = "ip_addresses.txt"

                    with open(input_file, "r") as f:
                        domains = f.readlines()

                    with open(output_file, "a+") as f:
                        总进度 = len(domains)
                        进度 = 0
                        for domain in domains:
                            ip = domain_to_ip(get_main(domain))
                            if ip:
                                if remain_domain == "y":
                                    f.write(f"{domain.strip()} : {ip}\n")
                                if remain_domain == "n":
                                    f.write(f"{ip}\n")
                            print(f"进度：{进度}/{总进度}")
                            进度 += 1
                if thread_choice == "y":

                    with open(input_file, "r") as f:
                        domains = f.readlines()

                    总进度 = len(domains)
                    进度 = 0
                    for domain in domains:
                        thread_domain_to_ip(get_main(domain))
                        print(f"进度：{进度}/{总进度}")
                        进度 += 1

                    print("域名转IP完毕")

            ############################批量检测存活#######################################
            if choice == '2':
                file_name = input("请输入文件名：")
                filter_urls(file_name)
                time.sleep(1)
            ############################批量检测存活#######################################

            ############################批量提取xray结果目标(去重)#######################################
            if choice == "3":#批量提取xray html中的IP

                file_name = input("请输入文件名(xxx.html)：")

                with open(file_name,"r+",encoding="utf-8") as input_file:
                    content = input_file.read()
                targets = re.findall('{"addr":"(.*?)","payload',content)

                unique_targets = []
                for i in targets:
                    target_ip = get_main(i)
                    if target_ip not in unique_targets:
                        unique_targets.append(target_ip)

                for i in unique_targets:
                    with open("xray_targets.txt","a+") as output_file:
                        output_file.write(i + "\n")
            ############################批量提取xray结果目标(去重)#######################################
            ############################批量解析排除重复ip#######################################
            if choice == "4":#批量解析排除重复ip
                choice_thread = input("是否多线程(y/n)：")
                if choice_thread == "y":
                    file_name = input("请输入文件名：")
                    remove_same_ip(file_name,1)#1代表多线程
                if choice_thread == "n":
                    file_name = input("请输入文件名：")
                    remove_same_ip(file_name,0)#0代表不多线程
            ############################批量解析排除重复ip#######################################
            ############################批量提取后台系统#########################################
            if choice == "5":#批量提取后台系统
                file_name = input("请输入文件名：")

                with open(file_name, "r+") as input_file:
                    sites = input_file.readlines()
                for url in sites:
                    url = url.strip()

                    if "http://" not in url and "https://" not in url:
                        url = "http://" + url

                    filter_back_platform(url)
                    time.sleep(3)
            ############################批量提取后台系统################
            ##########################域名IP排重######################
            if choice == "6":#域名IP排重
                file_name = input("请输入文件名：")

                with open(file_name, "r+") as input_file:
                    sites = input_file.readlines()

                extract_unique_domains_ips(sites,"unique_ip_domains.txt")
        ###################批量操作########################

        if opear == "3":#更新代理池
            print("---------------------------------")
            choice = input("(1)使用proxypool(需要到conf配置)\n(2)读当前文件代理：")
            if choice == '1':
                update_proxy_Bypool()
            if choice == '2':
                file_name= input("请输入文件名：")
                update_proxy_ByFile(file_name)

        if opear == "4":#盒子半自动化提交
            domain = input("请输入存在漏洞的域名：")
            type = {"1":"CSRF","2":"SQL注入","3":"反射型XSS","4":"信息泄露","5":"弱口令"}
            choice = input(f"请选择漏洞类型:{type}:")
            leak_type = type[choice]

            leak_url = input("请输入漏洞url:")
            vulbox_src_page(domain,leak_type,leak_url)


        if opear == "5":#补天自动化提交
            domain = input("请输入存在漏洞的域名：")
            type = {"1": "逻辑漏洞", "2": "SQL注入", "3": "XSS", "4": "信息泄露", "5": "弱口令","6":"代码执行"}
            choice = input(f"请选择漏洞类型:{type}:")
            leak_type = type[choice]

            leak_url = input("请输入漏洞url:")
            butian_src_page(domain, leak_type, leak_url)

        if opear == "6":#xray一键扫描
            choice = input("是否crawlergo自动进行爬取(y/n)(选择否则只监听)：")
            if choice == 'y':
                file_name = input("请输入文件名：")
                cookie_choice = input("是否导入cookie(y/n)：")
                if cookie_choice == "n":
                    with open(file_name, "r+") as input_file:
                        cmd = 0
                        for text in input_file.readlines():
                            data1 = text.strip('\n')
                            if "http://" not in data1 and "https://" not in data1:
                                data1 = "http://" + data1
                            scan_urls(data1,xray_path,crawlergo_path,cmd)
                            cmd = cmd + 1
                if cookie_choice == "y":
                    print("cookie请到xray_scan_urls.py中与config.yaml中自定义")
                    with open(file_name, "r+") as input_file:
                        cmd = 0
                        for text in input_file.readlines():
                            data1 = text.strip('\n')
                            if "http://" not in data1 and "https://" not in data1:
                                data1 = "http://" + data1
                            scan_urls_cookies(data1,xray_path,crawlergo_path,cmd)
                            cmd = cmd + 1
            if choice == "n":
                start_xray_listen(xray_path)
                print("正在监听端口62224")

        if opear == "7":#C段提取
            file_name = input("请输入文件名：")
            filter(file_name)

        if opear == "8":#cnvd半自动化提交
            from info.cnvd_commit import cnvd_src_page
            domain = input("请输入存在漏洞的域名：")
            type = {"1": "逻辑缺陷", "2": "SQL注入", "3": "XSS", "4": "信息泄露", "5": "弱口令", "6": "命令执行"}
            choice = input(f"请选择漏洞类型:{type}：")
            leak_type = type[choice]

            leak_url = input("请输入漏洞url：")
            cnvd_src_page(domain, leak_type, leak_url)
