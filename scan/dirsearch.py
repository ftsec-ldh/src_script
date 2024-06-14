import os

def dirscan(dirsearch_path, url):
    command = f'python "{dirsearch_path}dirsearch.py" -u "{url}"'
    os.system(f'start cmd.exe /K {command}')

