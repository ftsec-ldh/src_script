import socket,requests,re
from requests.exceptions import ConnectionError, Timeout, RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def scan_port_socket(ip, port, open_ports):
    socket.setdefaulttimeout(1)  # 设置默认超时时间
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
        result = s.connect_ex((ip, port))  # 尝试连接到指定的IP和端口
        if result == 0:
            open_ports.append(port)  # 如果端口开放，添加到列表中
        s.close()  # 关闭socket
    except Exception as e:
        print(f"Error checking port {port} on {ip}: {e}")

def scan_ports_socket(ip, ports):
    open_ports = []
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port_socket, args=(ip, port, open_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return open_ports

def scan_port_web(ip, port):
    url = f"http://{ip}:{port}"  # 构造URL
    try:
        response = requests.get(url, timeout=3)#发送GET请求
        content = response.text.strip()#获取网页内容并去除首尾空白
        if content:#如果网页内容不为空
            return port, True, "Content found"
        else:
            return port, False, "Empty content"
    except ConnectionError:
        return port, False, "ConnectionError"
    except Timeout:
        return port, False, "Timeout"
    except RequestException as e:
        return port, False, str(e)

def scan_web_ports(ip, ports):
    open_web_ports = []

    with ThreadPoolExecutor(max_workers=10) as executor:  # 创建线程池
        futures = [executor.submit(scan_port_web, ip, port) for port in ports]

        for future in as_completed(futures):
            port, is_open, status = future.result()
            if is_open:
                open_web_ports.append(port)
                print(f"Port {port} on {ip} is serving HTTP content.")
            else:
                print(f"Port {port} on {ip} is open but returned HTTP status {status}.")

    return open_web_ports
