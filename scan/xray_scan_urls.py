#!/usr/bin/python3
# coding: utf-8
import simplejson
import threading
import subprocess,os
import requests
import warnings
import json
from fake_useragent import UserAgent
from ruamel.yaml import YAML

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

def start_xray_listen(xray_path):
	if "xray.html" in os.listdir(xray_path):
		choice = input("发现存在xray.html，是否删除？(y/n)：")
		if choice == "y":
			os.remove(xray_path + "/xray.html")
		if choice == "n":
			exit()
	os.chdir(xray_path)
	command = f'xray_windows_amd64.exe webscan --listen 127.0.0.1:62224 --html-output xray.html'
	os.system(f'start cmd.exe /K {command}')

def scan_urls(data1,xray_path,crawlergo_path,cmd):
	if cmd == 0:
		start_xray_listen(xray_path)

		yaml = YAML()
		yaml.preserve_quotes = True
		yaml.indent(mapping=2, sequence=4, offset=2)

		# 读取配置文件
		with open(f"{xray_path}config.yaml", 'r', encoding='utf-8') as file:
			config_data = yaml.load(file)

		config_data['http']['headers']['Cookie'] = ""#清空Cookie

		with open(f"{xray_path}config.yaml", 'w', encoding='utf-8') as file:
			yaml.dump(config_data, file)

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

def scan_urls_cookies(data1,xray_path,crawlergo_path,cmd):

	Cookie = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaW4tdXNlciIsImlhdCI6MTcyMjYwODMxMiwiZXhwIjoxNzIyNjk0NzEyLCJpZCI6IjE4MiJ9.Qg_XGW9LWi2ebf8ZSctiR-BPMn-iUKNpNEaPEcnCw_A"

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
		"Token": Cookie
	}


	if cmd == 0:
		os.chdir(xray_path)
		yaml = YAML()
		yaml.preserve_quotes = True
		yaml.indent(mapping=2, sequence=4, offset=2)

		# 读取配置文件
		with open(f"{xray_path}config.yaml", 'r', encoding='utf-8') as file:
			config_data = yaml.load(file)

		config_data['http']['headers']['Cookie'] = Cookie

		with open(f"{xray_path}config.yaml", 'w', encoding='utf-8') as file:
			yaml.dump(config_data, file)

		command = f'xray_windows_amd64.exe webscan --listen 127.0.0.1:62224 --html-output xray.html'
		os.system(f'start cmd.exe /K {command}')

	target = data1
	cmd = [f"{crawlergo_path}crawlergo_win_amd64.exe","-t", "5","-f","smart","--fuzz-path","--custom-headers",json.dumps(get_random_headers()), "--request-proxy", "http://127.0.0.1:62224", "--push-pool-max", "10","--output-mode", "json","--custom-headers", simplejson.dumps(headers) , target]
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
