from info.api import get_main
from filter.socket_getIP import domain_to_ip
import re,threading

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

def thread_domain_to_ip(main,unique_ip_targets,line,进度,目标和):
    with open("无重ip.txt", "a+") as input_file:
        ip = domain_to_ip(main)
        if ip not in unique_ip_targets:
            input_file.write(line + "\n")
        unique_ip_targets.append(ip)

def remove_same_ip(filename,thread=0):
    if thread == 1:
        with open(filename, 'r') as input_file:
            进度 = 0
            目标和 = len(input_file.readlines())
            input_file.seek(0)#指针重新回到0
            unique_ip_targets = []
            threads = []
            for line in input_file:
                line = line.strip()#去除行尾的换行符和空格
                main = get_main(line)

                thread = threading.Thread(target=thread_domain_to_ip,args=[main,unique_ip_targets,line,进度,目标和])
                threads.append(thread)

            for i in threads:
                i.start()
                进度 += 1
                print(f"进度：{进度}/{目标和}")
    if thread == 0:
        with open(filename, 'r') as input_file:
            target_number = len(input_file.readlines())
            input_file.seek(0)#指针重新回到0
            unique_ip_targets = []
            进度 = 0
            for line in input_file:
                line = line.strip()#去除行尾的换行符和空格
                main = get_main(line)
                with open("无重ip.txt", "a+") as input_file:
                    ip = domain_to_ip(main)
                    if ip not in unique_ip_targets:
                        input_file.write(line + "\n")
                    unique_ip_targets.append(ip)
                print(f"进度：{进度}/{target_number}")
                进度 += 1
