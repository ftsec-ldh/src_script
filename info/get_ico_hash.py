import requests
import base64
import mmh3

def get_hash_byURL(url):
    r=requests.get(url,verify=False)
    r1=r.content
    r2=base64.encodebytes(r1)
    r3=mmh3.hash(r2)
    return "icon_hash = " + f"\"{str(r3)}\""

def get_hash_byFile(url):
    r1=url
    r2=base64.encodebytes(r1)
    r3=mmh3.hash(r2)
    return "icon_hash = " + f"\"{str(r3)}\""
