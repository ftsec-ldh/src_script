# 自写的src开源脚本
脚本推荐使用python3.8或以上  
selenium版本只支持4.0或以上  
windows-chrome版本为122  
linux-chrome版本为91.0.4472  
版本不一致请自行更改driver版本  
目前只有权重IP反查支持跨Win/Linux平台  
补天、漏洞盒子半自动化只支持Windows  
建议使用windows操作，如果非要使用Linux：推荐CentOS7
其他系统未经调试  
  
# Windows安装chrome拓展：  
  
https://googlechromelabs.github.io/chrome-for-testing/  

# CentOS7安装chrome拓展：
下载91.0.4472的版本
https://www.chromedownloads.net/chrome64linux-stable/  
`yum install ./google-chrome-stable_current_x86_64.rpm`  
即可安装  
  
谷歌爬取需设置代理走socks5(在info/google.py中设置)  
代理池更新：请使用前在conf/proxies.conf中设置好代理池接口  
  
如有疑问BUG或建议请到issus或pull requests中去发帖  
    
本工具旨在为信息收集提供便利性，仅用于学习行为，如使用者有任何侵权或违法犯罪行为与我无关！  
  
希望黑客们点个star！万分感谢！！！  
希望黑客们点个star！万分感谢！！！  
希望黑客们点个star！万分感谢！！！  
  
使用截图：  
![pic1](https://github.com/1607131160/src_script/assets/128038117/b1be191b-2352-42fd-acaf-f2605ca22bfa)  
![image](https://github.com/1607131160/src_script/assets/128038117/bf009fad-284f-46de-8888-a46956bd43d3)  
![image](https://github.com/1607131160/src_script/assets/128038117/2b031e6e-8102-4933-a27b-c009e9394371)  
![1ru3l-ho5tt](https://github.com/1607131160/src_script/assets/128038117/95e381dc-7c38-4d66-8dba-c88491debf14)  
# 更新内容 
  
版本：v0.1.6  
一、xray扫描功能添加cookie扫描后台选项  
二、添加补天自动提交行业配置并优化BUG  
  
版本：v0.1.5  
一、添加同一域名页面内容排重功能  
二、添加多线程方法选择  
  
版本：v0.1.4  
一、添加端口扫描并保存到txt功能  
二、添加解析域名ip排重功能  
  
版本：v0.1.3  
一、添加xray+crawlergo联合扫描功能  
二、添加批量提取xray-html结果目标功能
  
版本：v0.1.2  
一、添加URL批量提取权重网站(与方法2-1区别是提取的是主域名，方便用来做资产测绘)  
二、优化Linux跨平台glibc兼容性(降低chrome到91)  
  
版本：v0.1.1  
一.添加多级域名取主域名权重功能(防止二级域名及以上无权重，主域有权重的情况)<br>检查文件格式必须满足批量记录权重、单位名生成的txt格式  
  
版本：v0.1.0  
一.添加补天半自动化提交功能  
二.接口aiqicha_get返回字典添加area行政区划键值  
  
版本：v0.0.9  
一.增加dirsearch快捷扫描功能(到conf/dirsearch.conf设置dirsearch的路径)  
二.增加oneforall智能化扫描与csv智能化提取  
  
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
