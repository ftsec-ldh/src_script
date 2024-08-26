from bs4 import BeautifulSoup
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import re
import time
import random
import string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "socks5://127.0.0.1:10808",
           "https": "socks5://127.0.0.1:10808"}

def google_search():
    print("------------------------------------------")
    page_start = input("请输入爬取的起始页(例如0)：")
    page_end = input("请输入爬取的结尾页(例如100)：")
    content = input("请输入爬取的内容(例如谷歌语法)：")
    start = int(page_start) #起始页面
    end = int(page_end)
    search = content #搜索内容

    for i in range(start,end,10):
        random_string = ''.join(random.choices(string.ascii_letters,k=6))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.72 Safari/537.36',
            'Cookie': f'AEC=Ae3NU9P0YWNbhz2bnIQw2Tyuz7kshE860I-rc0-6gqMcgzYKMe3gPK00wO8; GOOGLE_ABUSE_EXEMPTION=ID=837693073b971bdf:TM=1709874541:C=r:IP=103.234.53.98-:S=rCPMrZ9DI-L6-2jhJimuOMA; NID=512=gelMvANPBelZm7ELmUVYiqD9y2IyjfQOSd4E0H-DPnCzxIIBCnAsG9viFQPQTzZB0ZXvwRzlqQmGj1Qy3MuxEOhaUKiGTj0qOVAV_I5jGwhqaiIkFy1-JMTZG4KTPMXib1P6GXOIUSQJ59AlcI6M1mB0QpIghdolrcQswnXJIFWJdf_jHb21pRGnXExpvS3wF_iEcLeYXlKKIO8YcoWWaJ9P3-hO; 1P_JAR=2024-03-08-07; DV=k2e1RXvkSxsYMMNiN6YW-ga{random_string}Rg',
            'Priority': 'u=0, i',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.google.com.hk/',
            'Accept': 'text/html,application/xhtml',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
            'Connection': 'close'
            }

        url = f"https://www.google.com.hk/search?vet=12ahUKEwjog8uPi-SEAxUBm1YBHVeOCOI4MhDErwIoAHoECAEQAw..i&ved=2ahUKEwiPsM67iOSEAxV50jQHHZw6AOMQqq4CegQIBhAE&bl=8ram&s=web&opi=89978449&sca_esv=5e1cf30a8e60a482&yv=3&q={search}&newwindow=1&ei=5LPqZY-uJ_mk0-kPnPWAmA4&start={i}&sa=N&sstk=AU0UtuDt-gRJLzJ_wStYtuD1ANyRr8Vj8obgWgTbg5CK7KMDWpU8wYRiDqB36mUgCJLDAkbtbBk4eN4tQ1mxepFS0MLDP1QyjFRKrMyq07J1E-vvpPPDVbjLSTe7LUNzyaR3q5Fdmt4Ilf3N7LTgwGQh8tUX0rWGZ81x5IDMEqNRBsEzKhRZown_WY4PoU3AMErylmxKm5NhfxQu3HQzQ9pB7C0dsy0H3EY2LF7V5xfealyXYCQ-l2ImkqoYlj0&asearch=arc&cs=0&async=arc_id:srp_160,ffilt:all,ve_name:MoreResultsContainer,use_ac:false,_id:arc-srp_160,_pms:s,_fmt:pc"
        res = requests.get(url,headers=headers,verify=False,timeout=10,proxies=proxies)
        html = res.text
        soup = BeautifulSoup(html,"html.parser")
        #print(html)
        all_a_tag = soup.find_all("a",jsname="UWckNb")
        for a_tag in all_a_tag:
            result = a_tag['href']
            with open("谷歌爬取结果.txt","a+") as output:
                #if "?" in result and "&" not in result:
                print(result)
                output.write(f"{a_tag['href']}\n")
        print(f"总共读取{end}页，当前读到{i+10}页")

        time.sleep(2)
