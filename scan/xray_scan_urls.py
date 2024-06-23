#!/usr/bin/python3
# coding: utf-8
import simplejson
import threading
import subprocess,os
import requests
import warnings
import json
from fake_useragent import UserAgent

ua = UserAgent()

warnings.filterwarnings(action='ignore')

def get_random_headers():
    headers = {'User-Agent': ua.random}
    return headers

def opt2File(paths):
	try:
		f = open('crawl_result.txt','a')
		f.write(paths + '\n')
	finally:
		f.close()

def opt2File2(subdomains):
	try:
		f = open('sub_domains.txt','a')
		f.write(subdomains + '\n')
	finally:
		f.close()

def scan_urls(data1,xray_path,crawlergo_path,cmd):
	if cmd == 0:
		os.chdir(xray_path)
		command = f'xray_windows_amd64.exe webscan --listen 127.0.0.1:62224 --html-output xray.html'
		os.system(f'start cmd.exe /K {command}')

	target = data1
	cmd = [f"{crawlergo_path}crawlergo_win_amd64.exe","-t", "5","-f","smart","--fuzz-path","--custom-headers",json.dumps(get_random_headers()), "--request-proxy", "http://127.0.0.1:62224", "--push-pool-max", "10","--output-mode", "json" , target]
	rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = rsp.communicate()
	try:
		result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
	except:
		return
	req_list = result["req_list"]
	sub_domain = result["sub_domain_list"]
	print(data1)
	print("[crawl ok]")
	try:
		for subd in sub_domain:
			opt2File2(subd)
	except:
		pass
	print("[scanning]")
