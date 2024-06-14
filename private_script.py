import re,platform,time,requests,os,glob
from info.api import crawl_company,get_main
from info.google import google_search
from info.update_proxies import update_proxy_Bypool,update_proxy_ByFile
from info.vulbox_commit import vulbox_login,vulbox_src_page
from info.get_ico_hash import get_hash_byURL,get_hash_byFile
from filter.socket_getIP import domain_to_ip
from filter.cls_repeat_ip import remove_duplicates
from filter.check_alive import filter_urls
from scan.dirsearch import dirscan
from scan.oneforall import domain_scan,domains_scan,filter_validIP,filter_validIPs

if __name__ == "__main__":
    while True:
        opear = input("(1)爬取谷歌内容\n(2)批量操作\n(3)更新代理池\n(4)盒子半自动化提交\n(5)取网站ico哈希值\n(6)目录扫描\n(7)子域收集\n请选择操作数：")
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
            choice = input('''(1)记录权重、单位名\n(2)批量域名取IP地址\n(3)批量排重\n(4)批量检测存活：''')
            if choice == "1":
                print("------------------------------------------")
                choice = input("(1)fofa\n(2)ip138\n请输入爬取的引擎：")
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
                            crawl_info = crawl_company(line,1)

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
                            crawl_info = crawl_company(line,0,proxies)#0代表用ip138
                            if "error" in str(crawl_info):
                                print(f"检测到代理池异常{str(crawl_info)}，已自动删除并开始重新爬取")
                                error_proxy = "".join(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:.+",str(crawl_info)))
                                proxies.remove(error_proxy + "\n")#删除报错的代理池
                            else:
                                break
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
            url = input("请输入要扫描的网站：")
            with open("conf/dirsearch.conf",encoding="utf-8") as input_file:
                dirsearch_path = input_file.read()
            if not dirsearch_path.endswith("/"):
                dirsearch_path = dirsearch_path + "\\"
            dirscan(dirsearch_path,url)

        if opear == "7":#子域收集
            with open("conf/oneforall.conf", encoding="utf-8") as input_file:
                oneforall_path = input_file.read()
            if not oneforall_path.endswith("/"):
                oneforall_path = oneforall_path + "\\"

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
                    #print(csv)
                    name = re.search(r'\\([^\\]+)\.csv$',csv).group(1)
                    if "all_subdomain" not in name:
                        print(name)
                print("-----------目前域名------------")
