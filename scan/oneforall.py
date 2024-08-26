import os
import ast
import pandas as pd
import glob
import subprocess
import numpy as np


def domain_scan(domain_search):# oneforall联动subfinder
    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)

    oneforall_path = config['oneforall_path']
    subfinder_path = config['subfinder_path']

    urls = set()

    command = ['python', f'{oneforall_path}/oneforall.py', '--valid=None', '--verify=False',f'--target={domain_search}', 'run']
    print(f"正在调用OneForAll收集域名：{domain_search}，请耐心等待！")
    try:
        subprocess.run(command, capture_output=True, text=True,encoding='utf-8')
    except Exception as e:
        print(f"输出：{e}")

    try:
        df = pd.read_csv(f"{oneforall_path}/results/{domain_search}.csv", encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(f"{oneforall_path}/results/{domain_search}.csv", encoding='latin1')

    valid_urls = df['subdomain'].tolist()
    for url in valid_urls:
        urls.add(url)

    command = [f'{subfinder_path}/subfinder.exe', '-d', domain_search]
    print(f"正在调用SubFinder收集域名：{domain_search}，请耐心等待！")
    result = subprocess.run(command, capture_output=True, text=True,encoding='utf-8')

    if result.stdout:#检查输出是否存在
        for url in result.stdout.split("\n"):
            if url:#确保url不为空
                urls.add(url)

    # 删除nan类型的float元素
    urls.discard(np.nan)
    urls.discard('')

    return urls
