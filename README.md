# 自写的src开源脚本
脚本推荐使用python3.8或以上  
selenium版本只支持4.0或以上  
windows-chrome版本为122，版本不一致请自行更改driver版本  
  
Windows安装chrome拓展：  
  
https://googlechromelabs.github.io/chrome-for-testing/  
  
Linux安装chrome拓展:  
  
`sudo yum install google-chrome-stable --nogpg`  
  
谷歌爬取需设置代理走socks5(在info/api.py中设置)  
代理池更新：请使用前在conf/proxies.conf中设置好代理池接口  
  
如有疑问BUG或建议请到issus或pull requests中去发帖  
    
本工具旨在为信息收集提供便利性，仅用于学习行为，如使用者有任何侵权或违法犯罪行为，作者概不负责  
使用截图：  
![pic1](https://github.com/1607131160/src_script/assets/128038117/b1be191b-2352-42fd-acaf-f2605ca22bfa)

版本：v0.0.8  
一.删除XRAY漏扫功能(主动扫描太鸡肋，索性直接移除该功能)  
二.批量操作增加去重、批量域名取IP、批量检测存活功能  
  
版本：v0.0.7  
一.优化漏洞盒子SRC信息提交速度  
二.api增加爱企查接口，盒子填写增加自动选择公司地区的功能  
  
版本：v0.0.6  
一.修复Linux的driver驱动路径读取问题  
二.增加xray批量扫描功能，支持Windows和Linux  
三.增加获取ico哈希功能  
四.更新代理池增加本地读取功能  

版本：v0.0.5  
一.增加代理池文件读取功能  
二.优化了交互文字显示格式  
  
版本：v0.0.4  
一.增加检测代理池多线程功能  
二.增加requirement.txt  
<br>
版本：v0.0.3  
一.解决了爬取过程中遇到代理池出错停止爬取的问题，如果代理池出错则自动删除并重新爬取  
二.增加漏洞盒子半自动化提交功能，根据域名自动填写提交信息  
三.优化代码逻辑，增加更多的异常检测，防止用户误输报错  
  
版本：v0.0.2  
一.增加selenium框架的跨平台检测，目前能于Linux/Windows系统中正常使用  
二.增加代理池爬取方法，防止请求频繁被拉黑(在conf/proxies.conf中设置好代理池接口)  
三.优化了用户交互异常判断  
  
版本：v0.0.1  
更新内容：  
1.批量爬取谷歌引擎搜索内容(默认代理走本机10808,如需更改请到info/api.py中更改)  
2.批量自动反查IP的域名并自动查询权重与公司名  
