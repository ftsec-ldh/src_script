import os,ast
import pandas as pd
import glob,subprocess
from urllib.parse import urlparse

# 保存排重后的域名到文件
def save_domains_to_file(domains, filename):
    with open(filename, 'w') as file:
        for domain in domains:
            file.write(domain + '\n')


def domain_scan(domain_search):#oneforall联动subfinder
    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)

    oneforall_path = config['oneforall_path']
    subfinder_path = config['subfinder_path']

    urls = set()

    command = ['python', f'{oneforall_path}\oneforall.py', '--valid=None', '--verify=False', f'--target={url}', 'run']
    print(f"即将调用OneForAll收集域名：{url}，请耐心等待！")
    subprocess.run(command, capture_output=True, text=True)
    try:
        df = pd.read_csv(f"{oneforall_path}\\results\\{domain_search}.csv", encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(f"{oneforall_path}\\results\\{domain_search}.csv", encoding='latin1')

    valid_urls = df['subdomain'].tolist()
    for url in valid_urls:
        urls.add(url)


    command = [f'{subfinder_path}\\subfinder.exe', '-d', domain_search]
    print(f"即将调用SubFinder收集域名：{domain_search}，请耐心等待！")
    result = subprocess.run(command, capture_output=True, text=True)
    for url in result.stdout.split("\n"):
        urls.add(url)
    urls.remove('')
    return urls



def domains_scan(file_name):
    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)
    oneforall_path = config['oneforall_path']

    command = f'python "{oneforall_path}oneforall.py" --valid=None --verify=False --targets {file_name} run'
    os.system(f'start cmd.exe /K {command}')


def filter_validIP(domain_name):

    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)
    oneforall_path = config['oneforall_path']

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

def filter_validIPs():
    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)
    oneforall_path = config['oneforall_path']

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
