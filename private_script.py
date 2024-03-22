import os
import requests
import re
from info.api import crawl_company
from info.google import google_search
from info.update_proxies import update_proxy_Bypool,update_proxy_ByFile
from info.vulbox_commit import vulbox_login,vulbox_src_page


if __name__ == "__main__":
    while True:
        opear = input("(1)爬取谷歌内容\n(2)批量操作\n(3)更新代理池\n(4)盒子半自动化提交\n请选择操作数：")
        if opear == "1":
            print("------------------------------------------")
            page_start = input("请输入爬取的起始页(例如0)：")
            page_end = input("请输入爬取的结尾页(例如100)：")
            crawl_content = input("请输入爬取的内容(例如谷歌语法)：")
            google_search(page_start,page_end,crawl_content)
        if opear == "2":
            print("------------------------------------------")
            choice = input('''批量记录权重、单位名(1)：''')
            if choice == "1":
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
                        crawl_info = crawl_company(line,proxies)
                        if "error" in str(crawl_info):
                            print(f"检测到代理池异常{str(crawl_info)}，已自动删除并开始重新爬取")
                            error_proxy = "".join(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:.+",str(crawl_info)))
                            proxies.remove(error_proxy + "\n")#删除报错的代理池
                        else:
                            break

        if opear == "3":
            print("---------------------------------")
            choice = input("(1)使用proxypool(需要到conf配置)\n(2)读当前文件代理：")
            if choice == '1':
                update_proxy_Bypool()
            if choice == '2':
                file_name= input("请输入文件名：")
                update_proxy_ByFile(file_name)

        if opear == "4":
            domain = input("请输入存在漏洞的域名：")
            type = {"1":"csrf","2":"sql注入","3":"xss","4":"信息泄露"}
            choice = input("请选择漏洞类型:(1)csrf;(2)sql注入;(3)xss;(4)信息泄露:")
            leak_type = type[choice]
            vulbox_src_page(domain,leak_type)


