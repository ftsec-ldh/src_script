import requests
import threading
import sys
import os
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_alive(url):
    try:
        if "http:" not in url:
            url = "http://" + url
        response = requests.head(url, timeout=2,verify=False)
        return True
    except requests.exceptions.RequestException:
        return False

class URLChecker(threading.Thread):
    def __init__(self, url, output_file):
        threading.Thread.__init__(self)
        self.url = url
        self.output_file = output_file

    def run(self):
        if "http://" not in self.url and "https://" not in self.url:
            self.url = "http://" + self.url
        if check_alive(self.url):
            print(f"{self.url} is alive")
            with open(self.output_file, 'a') as file:
                file.write(f"{self.url}\n")
        else:
            print(f"{self.url} is dead")

def filter_urls(filename):
    alive_urls = []
    with open(filename, 'r') as file:
        for line in file:
            url = line.strip()
            thread = URLChecker(url, 'alive.txt')
            thread.start()
