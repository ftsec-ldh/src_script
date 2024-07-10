import os

def dirscan(dirsearch_path, file_name,thread,language,proxy):
    if len(proxy) == 0:
        command = f'python "{dirsearch_path}dirsearch.py" -l "{file_name}" -t {thread} -e {language}'
        os.system(f'start cmd.exe /K {command}')

    if len(proxy) != 0:
        command = f'python "{dirsearch_path}dirsearch.py" -l "{file_name}" -t {thread} -e {language} --proxy {proxy}'
        os.system(f'start cmd.exe /K {command}')

#扫描完毕提示Task Completed
