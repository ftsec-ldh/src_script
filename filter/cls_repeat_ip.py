from info.api import get_main
from filter.socket_getIP import domain_to_ip
import re

def remove_duplicates(filename):
    lines_seen = set()
    output_filename = filename.split('.')[0] + "_nodupes.txt"

    with open(filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        for line in input_file:
            line = line.strip()  # 去除行尾的换行符和空格
            if line not in lines_seen:
                output_file.write(line + '\n')
                lines_seen.add(line)

    print("去除重复行完成！保存为：", output_filename)

def remove_same_ip(filename):
    with open(filename, 'r') as input_file:

        target_number = len(input_file.readlines())
        input_file.seek(0)#指针重新回到0

        unique_ip_targets = []
        进度 = 0
        for line in input_file:
            line = line.strip()#去除行尾的换行符和空格
            main = get_main(line)

            ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
            ip_match = re.search(ip_pattern, main)
            with open("无重ip.txt", "a+") as input_file:
                if ip_match:#说明是ip
                    if main not in unique_ip_targets:
                        input_file.write(line + "\n")
                    unique_ip_targets.append(main)
                        #unique_ip_targets.append(line)
                else:#说明是域名
                    ip = domain_to_ip(main)
                    if ip not in unique_ip_targets:
                        input_file.write(line + "\n")
                        #unique_targets.append(line)
                    unique_ip_targets.append(ip)
                print(f"进度：{进度}/{target_number}")
                进度 += 1
