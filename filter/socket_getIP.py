
import socket
def domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain.strip())
        return ip
    except socket.error as e:
        print(f"Error converting {domain} to IP: {e}")
        return None
