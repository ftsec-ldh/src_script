import socket
import vthread


def domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain.strip())
        return ip
    except socket.error as e:
        print(f"Error converting {domain} to IP: {e}")
        return None

@vthread.pool(1000)
def thread_domain_to_ip(domain):
    with open("ip_addresses.txt","a+") as output_file:
        try:
            ip = socket.gethostbyname(domain.strip())
            output_file.write(ip + "\n")
        except socket.error as e:
            print(f"Error converting {domain} to IP: {e}")
            return None
