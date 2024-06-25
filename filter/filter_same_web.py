import requests
import hashlib
from urllib.parse import urlparse
import re


def get_main_domain(domain):
    # 移除域名中的端口号（如果有）
    domain = domain.split(':')[0]
    parts = domain.split('.')
    if len(parts) < 2:
        return domain
    if parts[-1] in ('cn', 'com', 'net', 'org', 'gov', 'edu'):
        return '.'.join(parts[-3:]) if parts[-2] in ('com', 'net', 'org', 'gov', 'edu') else '.'.join(parts[-2:])
    else:
        return '.'.join(parts[-2:])

def get_main(url):
    if "http://" not in url and "https://" not in url:
        url = "http://" + url
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    ip_match = re.search(ip_pattern, url)
    if ip_match:#说明是ip
        main_part = ip_match.group()
    else:
        domain_pattern = r"https?://([^:/]+)"#提取域名
        domain_match = re.findall(domain_pattern, url)
        if domain_match:
            main_part = domain_match[0]
        else:
            main_part = ""
    return main_part

def fetch_content(url):
    """ Fetch the content from a URL and return the hash of the content. """
    try:
        response = requests.get(url, timeout=10)  # Adjust timeout as necessary
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return hashlib.md5(response.content).hexdigest()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def compare_sites(site_list, output_file):
    """ Compare the content of different sites within the same domain and save unique sites to a file. """
    domain_content_dict = {}
    with open(output_file, "a+") as file:
        for site in site_list:
            domain_name = get_main_domain(get_main(site))
            content_hash = fetch_content(site)
            if content_hash:
                if domain_name not in domain_content_dict:
                    domain_content_dict[domain_name] = {}
                if content_hash not in domain_content_dict[domain_name]:
                    domain_content_dict[domain_name][content_hash] = site
                    file.write(site + '\n')
                    print(f"Keeping {site} as unique under domain {domain_name}.")
                else:
                    print(f"Duplicate found under {domain_name}: {site} is the same as {domain_content_dict[domain_name][content_hash]}")
            else:
                print(f"Failed to fetch content for {site}")

