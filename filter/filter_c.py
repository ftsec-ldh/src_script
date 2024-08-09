import pandas as pd
from ipaddress import ip_address, ip_network
from collections import defaultdict


def read_ips(file_path):
    """ 从文件中读取IP地址列表 """
    with open(file_path, 'r') as file:
        ips = [line.strip() for line in file if line.strip()]
    return ips


def classify_ips(ips):
    """ 将IP分到各自的C段，并筛选出至少有两个IP的C段 """
    networks = defaultdict(list)
    for ip in ips:
        ip_obj = ip_address(ip)
        network = ip_network(f'{ip_obj}/24', strict=False)
        networks[str(network)].append(str(ip_obj))

    # 只保留IP数量两个或以上的C段
    return {net: ips for net, ips in networks.items() if len(ips) > 1}


def save_to_excel(data, output_file):
    """ 保存数据到Excel文件 """
    rows = []
    for c_segment, ip_list in data.items():
        rows.append({'C段': c_segment, 'IP': '\n'.join(ip_list), 'IP个数': len(ip_list)})
    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)


def filter(file_name):
    input_file = file_name  # 输入文件名
    output_file = 'c段.xlsx'  # 输出Excel文件名

    ips = read_ips(input_file)
    classified_data = classify_ips(ips)
    save_to_excel(classified_data, output_file)
    print("IP分类已保存到Excel文件。")

