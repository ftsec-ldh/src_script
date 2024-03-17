import os
import requests
import re
from info.api import*
from info.google import google_search
from info.update_proxies import update_proxy


if __name__ == "__main__":
    while True:
        opear = input("爬取谷歌内容(1)；批量操作(2)；更新代理池(3)：")
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
                file_name = input("请输入文件名：")
                try:
                    with open(file_name,"r+") as input:
                        lines = input.readlines()
                except FileNotFoundError:
                    print("不存在该文件")
                    continue

                for line in lines:
                    line = line.strip()
                    url = line
                    if re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}",line):#检测到IP自动反查域名
                        domain = get_domain_byIP(line)
                        if domain:
                            name = get_company(line)
                            content = f"ip：{url}，域名：{domain},公司名：{name}, 权重：{get_rank(domain)}"
                            print(content, end="\n")
                            if "-" not in name:
                                with open("公司权重.txt", "a+") as output:
                                    output.write(content + "\n")
                            continue
                        else:
                            print(line.replace("http://","").replace("https://","") + "未绑定域名，跳过此次查询",end="\n")
                            continue
                    name = get_company(line)
                    content = f"站点：{url},公司名：{name}, 权重：{get_rank(line)}"
                    print(content,end="\n")
                    if "-" not in name:
                        with open("公司权重.txt","a+") as output:
                            output.write(content + "\n")
        if opear == "3":
            update_proxy()
