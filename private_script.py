import re,platform,time,requests,os,glob,threading
from info.api import crawl_company,get_main,extract_main_domain,get_rank
from info.google import google_search
from info.update_proxies import update_proxy_Bypool,update_proxy_ByFile
from info.vulbox_commit import vulbox_login,vulbox_src_page
from info.butian_commit import butian_login,butian_src_page
from info.get_ico_hash import get_hash_byURL,get_hash_byFile
from filter.socket_getIP import domain_to_ip
from filter.cls_repeat_ip import remove_duplicates,remove_same_ip
from filter.check_alive import filter_urls
from filter.filter_same_web import compare_sites,thread_compare_sites
from scan.dirsearch import dirscan
from scan.oneforall import domain_scan,domains_scan,filter_validIP,filter_validIPs
from scan.xray_scan_urls import scan_urls,scan_urls_cookies
from scan.port_scan import scan_ports_socket,scan_web_ports,thread_scan_http

with open("conf/dirsearch.conf", encoding="utf-8") as input_file:
    dirsearch_path = input_file.read()
if not dirsearch_path.endswith("/"):
    dirsearch_path = dirsearch_path + "\\"

with open("conf/oneforall.conf", encoding="utf-8") as input_file:
    oneforall_path = input_file.read()
if not oneforall_path.endswith("/"):
    oneforall_path = oneforall_path + "\\"

with open("conf/xray.conf", encoding="utf-8") as input_file:
    xray_path = input_file.read()
if not xray_path.endswith("/"):
    xray_path = xray_path + "\\"

with open("conf/crawlergo.conf", encoding="utf-8") as input_file:
    crawlergo_path = input_file.read()
if not crawlergo_path.endswith("/"):
    crawlergo_path = crawlergo_path + "\\"

if __name__ == "__main__":
    while True:
        opear = input("(1)爬取谷歌内容\n(2)批量操作\n(3)更新代理池\n(4)盒子半自动化提交\n(5)取网站ico哈希值\n(6)目录扫描\n(7)子域收集\n(8)补天半自动化提交\n(9)xray一键扫描\n请选择操作数：")
        #################爬谷歌内容###########################
        if opear == "1":
            print("------------------------------------------")
            page_start = input("请输入爬取的起始页(例如0)：")
            page_end = input("请输入爬取的结尾页(例如100)：")
            crawl_content = input("请输入爬取的内容(例如谷歌语法)：")
            google_search(page_start,page_end,crawl_content)
       ###################爬谷歌内容########################
       ###################批量操作########################
        if opear == "2":
            print("------------------------------------------")
            choice = input('''(1)批量取权重、公司名\n(2)批量域名取IP地址\n(3)批量排重\n(4)批量检测存活\n(5)根域名复查权重(只支持方法1导出的文件格式)\n(6)批量提取权重站点
(7)批量提取xray结果目标\n(8)批量扫描web端口\n(9)解析排除重复IP\n(10)批量排除相同页面的子域：''')
            if choice == "1":
                print("------------------------------------------")
                choice = input("(1)fofa(有次数限制)\n(2)ip138(需要代理池防拉黑)\n请输入爬取的引擎：")
                if choice == '1':
                 ############################直接爬fofa##################################
                    file_name = input("请输入文件名：")
                    try:
                        with open(file_name, "r+") as file_name_input:
                            lines = file_name_input.readlines()  # 读要爬的URL列表
                    except FileNotFoundError:
                        print("不存在该文件")

                    for line in lines:
                        line = line.strip()
                        crawl_company(line,1)#这里没有传递proxies，故不启用代理池

                ############################直接爬fofa########################################
                ############################代理池爬ip138取IP##################################
                if choice == '2':
                    try:
                        with open("proxies.txt", "r+") as proxies_input:
                            proxies = proxies_input.readlines()#读代理文件
                    except FileNotFoundError:
                        print("未检测到代理池文件，请先更新代理池")

                    file_name = input("请输入文件名：")
                    try:
                        with open(file_name, "r+") as file_name_input:
                            lines = file_name_input.readlines()#读要爬的URL列表
                    except FileNotFoundError:
                        print("不存在该文件")

                    for line in lines:
                        while True:
                            line = line.strip()
                            crawl_info = crawl_company(line,0,proxies,0)#arg2=0代表用ip138,arg4=0代表不复查主域
                            if "error" in str(crawl_info):
                                print(f"检测到代理池异常{str(crawl_info)}，已自动删除并开始重新爬取")
                                error_proxy = "".join(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:.+",str(crawl_info)))
                                proxies.remove(error_proxy + "\n")#删除报错的代理池
                            else:
                                break
                    exit()
                ############################代理池爬ip138取IP##################################
            ############################批量域名取IP#######################################
            if choice == "2":
                input_file = input("请输入文件名：")
                remain_domain = input("是否保留域名(y/n)：")
                output_file = "ip_addresses.txt"

                with open(input_file, "r") as f:
                    domains = f.readlines()

                with open(output_file, "w") as f:
                    for domain in domains:
                        ip = domain_to_ip(get_main(domain))
                        if ip:
                            if remain_domain == "y":
                                f.write(f"{domain.strip()} : {ip}\n")
                            if remain_domain == "n":
                                f.write(f"{ip}\n")
                print("域名转IP完毕")
            ############################批量域名取IP#######################################
            ############################批量排重#######################################
            if choice == "3":
                input_file = input("请输入需要排重的文件：")
                remove_duplicates(input_file)
            ############################批量排重#######################################
            ############################批量检测存活#######################################
            if choice == '4':
                file_name = input("请输入文件名：")
                filter_urls(file_name)
                time.sleep(1)
            ############################批量检测存活#######################################
            ############################根域名复查权重#######################################
            if choice == "5":#根域名复查权重，防止主域名比二级域名权重高
                file_name = input("请输入文件名：")
                try:
                    with open(file_name, "r+") as file_name_input:
                        lines = file_name_input.readlines()#读要爬的URL列表
                except FileNotFoundError:
                    print("不存在该文件")

                unique_lines = []
                for line in lines:
                    line = line.strip()
                    main_domain = extract_main_domain(line)
                    if main_domain not in unique_lines:
                        unique_lines.append(main_domain)#将主域名排重


                for unique_line in unique_lines:
                    crawl_company(unique_line,0,0,1)

            ############################根域名复查权重#######################################
            ############################批量提取权重网站主域名#######################################
            if choice == "6":#批量提取权重网站主域名
                file_name = input("请输入文件名：")
                try:
                    with open(file_name, "r+") as file_name_input:
                        lines = file_name_input.readlines()  # 读要爬的URL列表
                except FileNotFoundError:
                    print("不存在该文件")

                unique_lines = []
                for line in lines:
                    line = line.strip().replace("https://","").replace("http://","")
                    line = get_main(line)
                    line = extract_main_domain(line)
                    if line not in unique_lines:
                        unique_lines.append(line)#将主域名排重

                for unique_line in unique_lines:
                    ranks = get_rank(unique_line)
                    try:
                        if int(ranks[0]) != 0 or int(ranks[1]) != 0 or int(ranks[2])!= 0 or int(ranks[3]) != 0 or int(ranks[4]) != 0 or int(ranks[5]) >= 3:
                            with open("权重网站集合.txt","a+") as output_file:
                                output_file.write(f"{unique_line}\n")
                    except Exception:
                        pass
                    print(f"{unique_line}{ranks}")
            ############################批量提取权重网站主域名#######################################
            ############################批量提取xray结果目标(去重)#######################################
            if choice == "7":#批量提取xray html中的IP

                file_name = input("请输入文件名(xxx.html)：")

                with open(file_name,"r+",encoding="utf-8") as input_file:
                    content = input_file.read()
                targets = re.findall('\{"addr":"(.*?)","payload',content)

                unique_targets = []
                for i in targets:
                    target_ip = get_main(i)
                    if target_ip not in unique_targets:
                        unique_targets.append(target_ip)

                for i in unique_targets:
                    with open("xray_targets.txt","a+") as output_file:
                        output_file.write(i + "\n")
            ############################批量提取xray结果目标(去重)#######################################
            ############################批量扫描web端口#######################################
            if choice == "8":#批量扫描web端口
                choice_thread = input("是否多线程(y/n)：")

                if choice_thread == "n":
                    file_name = input("请输入文件名：")
                    with open(file_name,"r+") as input_file:
                        urls = input_file.readlines()

                    port_number = [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 443, 4430, 8443, 9043, 8080, 8081, 8082,
                                   8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090, 8161, 8001, 8002, 8003, 7001,
                                   7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010, 5443, 9999, 8888, 8181, 8180,
                                   888, 9443, 4443, 4433, 3443, 9000, 9200, 10443]#HTTP端口

                    for line in urls:
                        ip_address = get_main(line).strip()
                        open_ports = scan_ports_socket(ip_address, port_number)
                        for i in scan_web_ports(ip_address, open_ports):
                            with open("open_web_ports.txt", "a+") as output_file:
                                output_file.write(f"{ip_address}:{i}\n")

                if choice_thread == "y":
                    file_name = input("请输入文件名：")
                    with open(file_name, "r+") as input_file:
                        urls = input_file.readlines()

                    port_number = [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 443, 4430, 8443, 9043, 8080, 8081, 8082,
                                   8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090, 8161, 8001, 8002, 8003, 7001,
                                   7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010, 5443, 9999, 8888, 8181, 8180,
                                   888, 9443, 4443, 4433, 3443, 9000, 9200, 10443]#HTTP端口
                    threads = []
                    for line in urls:
                        thread_scan_http(line,port_number)

            ############################批量扫描web端口#######################################
            ############################批量解析排除重复ip#######################################
            if choice == "9":#批量解析排除重复ip
                choice_thread = input("是否多线程(y/n)：")
                if choice_thread == "y":
                    file_name = input("请输入文件名：")
                    remove_same_ip(file_name,1)#1代表多线程
                if choice_thread == "n":
                    file_name = input("请输入文件名：")
                    remove_same_ip(file_name,0)#0代表不多线程
            ############################批量解析排除重复ip#######################################
            ############################批量排除相同页面的子域#######################################
            if choice == "10":#批量排除相同页面的子域
                thread_choice = input("是否多线程(y/n)：")
                if thread_choice == "n":
                    file_name = input("请输入文件名：")

                    with open(file_name, "r+") as input_file:
                        sites = input_file.readlines()
                    sites_list = []

                    for i in sites:
                        i = i.strip()
                        if "http://" not in i and "https://" not in i:
                            i = "http://" + i
                        sites_list.append(i)

                    compare_sites(sites_list, "unique_sites.txt")

                if thread_choice == "y":
                    file_name = input("请输入文件名：")

                    with open(file_name, "r+") as input_file:
                        sites = input_file.readlines()
                    sites_list = []

                    for i in sites:
                        i = i.strip()
                        if "http://" not in i and "https://" not in i:
                            i = "http://" + i
                        sites_list.append(i)

                    thread_compare_sites(sites_list, "unique_sites.txt")


            ############################批量排除相同页面的子域#######################################
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


        if opear == "5":#取网站ico哈希值
            choice = input("(1)本地文件读取\n(2)网页读取：")

            if choice == "1":
                file_name = input("请输入文件名:")
                with open(file_name,"rb") as ico:
                    ico_content = ico.read()
                print("-----------Web-Hash-----------")
                print(get_hash_byFile(ico_content))
                print("-----------Web-Hash-----------")

            if choice == "2":
                url = input("请输入favicon.ico地址：")
                if "http://" not in url and "https://" not in url:
                    url = "http://" + url
                print("-----------Web-Hash-----------")
                print(get_hash_byURL(url))
                print("-----------Web-Hash-----------")


        if opear == "6":#目录扫描
            url = input("要扫描的网站：")
            thread = input("线程数：")
            language = input("扫描类型(1)php (2)asp (3)jsp (4)全部：")
            proxies = input("http代理(不走代理填空即可,例如:127.0.0.1:10809)：")
            if language == '1':
                language = "php"
            elif language == '2':
                language = "asp"
            elif language == '3':
                language = "jsp"
            elif language == '4':
                language = "*"
            else:
                print("请输入正确的类型")
                continue
            dirscan(dirsearch_path,url,thread,language,proxies)#正式开始扫描

        if opear == "7":#子域收集
            choice = input("(1)oneforall单目标扫描\n(2)oneforall多目标扫描\n(3)提取单个域名\n(4)提取所有域名\n(5)查看目前收集域名：")
            if choice == "1":
                url = input("请输入要收集的域名：")
                domain_scan(oneforall_path, url)
            if choice == "2":
                file_name = input("请输入文件名：")
                domains_scan(oneforall_path,file_name)
            if choice == "3":
                domain_name = input("请输入单个域名：")
                filter_validIP(oneforall_path,domain_name)
            if choice == "4":
                filter_validIPs(oneforall_path)
            if choice == "5":
                print("-----------目前域名------------")
                csv_files = glob.glob(f'{oneforall_path}results\*.csv')
                for csv in csv_files:
                    name = re.search(r'\\([^\\]+)\.csv$',csv).group(1)
                    if "all_subdomain" not in name:
                        print(name)
                print("-----------目前域名------------")
        if opear == "8":#补天自动化提交
            domain = input("请输入存在漏洞的域名：")
            type = {"1": "逻辑漏洞", "2": "SQL注入", "3": "XSS", "4": "信息泄露", "5": "弱口令","6":"代码执行"}
            choice = input(f"请选择漏洞类型:{type}:")
            leak_type = type[choice]

            leak_url = input("请输入漏洞url:")
            butian_src_page(domain, leak_type, leak_url)

        if opear == "9":#xray一键扫描
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
