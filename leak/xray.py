import subprocess
import os


def windows_xray_scan(file_name):
    with open(file_name,'r+') as file:
        list = [www.strip() for www in file.readlines()]

    for ip in list:
        exp = ((r"xray_windows_amd64.exe webscan --basic-crawler {0}/ --html-output {1}.html").format(ip,ip))
        subprocess.Popen(["start", "cmd", "/k", f"cd {os.getcwd()}\leak && {exp}"], shell=True)

def Linux_xray_scan(file_name):
    with open(file_name,'r+') as file:
        list = [www.strip() for www in file.readlines()]

    for ip in list:
        exp = (("./leak/xray webscan --basic-crawler {0}/ --html-output {1}.html").format(ip, ip))
        os.system(exp)
        print(f"正在扫描{ip}")