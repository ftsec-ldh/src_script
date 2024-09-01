import subprocess,ast,os,shutil,re
import pandas as pd

def remove_common_items(list1, list2):
    # 使用列表推导式从list2中移除在list1中出现的元素
    result_list = [item for item in list2 if item not in list1]
    return result_list

def get_main(url):
    if "http://" not in url and "https://" not in url:
        url = "http://" + url
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    ip_match = re.search(ip_pattern, url)
    if ip_match:#说明是ip
        main_part = ip_match.group()
    else:
        domain_pattern = r"https?://([^:/]+)"#提取域名
        domain_match = re.findall(domain_pattern, url)
        if domain_match:
            main_part = domain_match[0]
        else:
            main_part = ""
    return main_part

def extract_fail_urls(excel_path):#过滤失败的IP
    df = pd.read_excel(excel_path)
    filtered_df = df[df['status'] == '-']
    return filtered_df['Url'].tolist()

def extract_success_urls(excel_path):#过滤成功的IP
    df = pd.read_excel(excel_path)
    filtered_df = df[df['status'] != '-']
    return filtered_df['Url'].tolist()


def find_latest(dir_path):#由于finger不能指定生成文件名，所以检测生成最新的xlsx
    latest_time = 0
    latest_file = None

    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)

        if os.path.isfile(full_path):
            creation_time = os.path.getctime(full_path)

            if creation_time > latest_time:
                latest_time = creation_time
                latest_file = filename

    return latest_file

def domains_cms(file_name):

    with open("conf/config.conf", encoding="utf-8") as config_file:
        config = config_file.read()
        config = ast.literal_eval(config)

    finger_path = config['finger_path']
    thread = input("线程数：")

    with open(f"{finger_path}/config/config.py","r",encoding="utf-8") as finger_config_file:
        config_lines = finger_config_file.readlines()

    for num,line in enumerate(config_lines):
        if "threads" in line:
            config_lines[num] = f"threads = {thread}"

    with open(f"{finger_path}/config/config.py","w",encoding="utf-8") as finger_config_outfile:
        finger_config_outfile.writelines(config_lines)

    command = ['python', f'{finger_path}/Finger.py', '-f', file_name]
    print(f"正在收集指纹信息，请耐心等待！")
    try:
        subprocess.run(command, capture_output=True, text=True,encoding='utf-8')
    except Exception as e:
        print(f"输出：{e}")
    lateast_file_name = find_latest(f"{finger_path}/output")
    shutil.move(f"{finger_path}/output/{lateast_file_name}",f"./{file_name.replace('.txt','.xlsx')}")
    print("收集完毕")
    fail_domains = []
    for domain in extract_fail_urls(f"{file_name.replace('.txt','.xlsx')}"):
        fail_domains.append(get_main(domain))

    success_domains = []
    for domain in extract_success_urls(f"{file_name.replace('.txt', '.xlsx')}"):
        success_domains.append(get_main(domain))

    fail_domains_final = remove_common_items(success_domains, fail_domains)#过滤出最终的失败域名列表
    with open(f"{file_name.replace('.txt', '')}失败域名.txt","a") as fail_domains_file:
        for domain in fail_domains_final:
            fail_domains_file.write(domain + "\n")


