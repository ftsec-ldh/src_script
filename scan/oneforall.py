import os
import pandas as pd
import glob
from urllib.parse import urlparse

# 读取文件中的URLs
def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# 提取并排重域名，优先保留HTTPS
def extract_unique_domains(urls):
    domain_dict = {}
    for url in urls:
        parsed_url = urlparse(url.strip())
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc

        # 如果当前域名不存在，或者存在但当前是HTTPS则更新/添加
        if netloc not in domain_dict or scheme == 'https':
            domain_dict[netloc] = url.strip()

    return domain_dict.values()

# 保存排重后的域名到文件
def save_domains_to_file(domains, filename):
    with open(filename, 'w') as file:
        for domain in domains:
            file.write(domain + '\n')


def domain_scan(oneforall_path,url):
    command = f'python "{oneforall_path}oneforall.py" --target {url} run'
    os.system(f'start cmd.exe /K {command}')

def domains_scan(oneforall_path,file_name):
    command = f'python "{oneforall_path}oneforall.py" --targets {file_name} run'
    os.system(f'start cmd.exe /K {command}')

def filter_validIP(oneforall_path,domain_name):
    urls = []
    try:
        df = pd.read_csv(f"{oneforall_path}results\\{domain_name}.csv", encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(f"{oneforall_path}results\\{domain_name}.csv", encoding='latin1')

    valid_urls = df[df['status'].notnull()]['url']
    urls.extend(valid_urls)
    urls = extract_unique_domains(urls)#HTTPS和HTTP有重复就优先保留HTTPS
    with open(f'{domain_name}.txt', 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')
    print("-------------提取信息-------------")
    print("提取完毕!!!!!!!!!!!!!")
    print("-------------提取信息-------------")

def filter_validIPs(oneforall_path):
    csv_files = glob.glob(f'{oneforall_path}results\*.csv')
    urls = []
    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding='latin1')

        valid_urls = df[df['status'].notnull()]['url']
        urls.extend(valid_urls)
    unique_domains = extract_unique_domains(urls)
    save_domains_to_file(unique_domains, "valid_domains.txt")
    print("-------------提取信息-------------")
    print("提取完毕!!!!!!!!!!!!!")
    print("-------------提取信息-------------")
