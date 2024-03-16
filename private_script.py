import os
import requests
import re
from info.api import*


if __name__ == "__main__":
    opear = input("单个操作(1)；批量操作(2)：")
    if opear == "2":
        print("------------------------------------------")
        print('''批量记录权重、单位名(1)：''')
        choice = input("")
        if choice == "1":
            file_name = input("请输入文件名：")
            with open(file_name,"r+") as input:
                for i in input:
                    i = i.strip()
                    url = i
                    if re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}",i):#检测到IP自动反查域名
                        domain = get_domain_byIP(i)
                        if domain:
                            print(f"ip：{url}，域名：{domain},公司名：{get_company(domain)}, 权重：{get_rank(domain)}", end="\n")
                            continue
                        else:
                            print(i.replace("http://","").replace("https://","") + "未绑定域名，跳过此次查询",end="\n")
                            continue
                    print(f"站点：{url},公司名：{get_company(i)}, 权重：{get_rank(i)}",end="\n")
