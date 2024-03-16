import os
import requests
import re
from info.api import*
from info.google import google_search


if __name__ == "__main__":
    opear = input("爬取谷歌内容(1)；批量操作(2)：")
    if opear == "1":
        print("------------------------------------------")
        page_start = input("请输入爬取的起始页(例如0)：")
        page_end = input("请输入爬取的结尾页(例如100)：")
        crawl_content = input("请输入爬取的内容(例如谷歌语法)：")
        google_search(page_start,page_end,crawl_content)
    if opear == "2":
        print("------------------------------------------")
        print('''批量记录权重、单位名(1)：''')
        choice = input("")
        if choice == "1":
            file_name = input("请输入文件名：")
            with open(file_name,"r+") as input:
                lines = input.readlines()

            for line in lines:
                line = line.strip()
                url = line
                if re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}",i):#检测到IP自动反查域名
                    domain = get_domain_byIP(line)
                    if domain:
                        print(f"ip：{url}，域名：{domain},公司名：{get_company(domain)}, 权重：{get_rank(domain)}", end="\n")
                        continue
                    else:
                        print(line.replace("http://","").replace("https://","") + "未绑定域名，跳过此次查询",end="\n")
                        continue
                print(f"站点：{url},公司名：{get_company(line)}, 权重：{get_rank(line)}",end="\n")
