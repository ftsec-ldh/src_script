# src_script
#自写的src开源脚本
脚本推荐使用python3.8或以上  
selenium版本只支持4.0或以上  
windows-chrome版本为122，版本不一致请自行更改driver版本  
Linux安装chrome拓展:  <br>
`sudo yum install google-chrome-stable --nogpg`  <br>
谷歌爬取需设置代理走socks(在info/api.py中设置)  
代理池更新：请使用前在conf/proxies.conf中设置好代理池接口  
  
如有疑问BUG或建议请到issus或pull requests中去发帖  
    
本工具旨在为信息收集提供便利性，仅用于学习行为，如使用者有任何侵权或违法犯罪行为，作者概不负责<br>
  
版本：v0.0.6<br>
一.修复Linux的driver驱动路径读取问题<br>
二.增加xray批量扫描功能，支持Windows和Linux<br>
三.增加获取ico哈希功能<br>
四.更新代理池增加本地读取功能<br>

版本：v0.0.5<br>
一.增加代理池文件读取功能<br>
二.优化了交互文字显示格式<br>
  
版本：v0.0.4<br>
一.增加检测代理池多线程功能<br>
二.增加requirement.txt<br>
<br>
版本：v0.0.3<br>
一.解决了爬取过程中遇到代理池出错停止爬取的问题，如果代理池出错则自动删除并重新爬取<br>
二.增加漏洞盒子半自动化提交功能，根据域名自动填写提交信息<br>
三.优化代码逻辑，增加更多的异常检测，防止用户误输报错<br>
<br>
版本：v0.0.2<br>
一.增加selenium框架的跨平台检测，目前能于Linux/Windows系统中正常使用<br>
二.增加代理池爬取方法，防止请求频繁被拉黑(在conf/proxies.conf中设置好代理池接口)<br>
三.优化了用户交互异常判断<br>
<br>
版本：v0.0.1<br>
更新内容：<br>
1.批量爬取谷歌引擎搜索内容(默认代理走本机10808,如需更改请到info/api.py中更改)<br>
2.批量自动反查IP的域名并自动查询权重与公司名<br>
