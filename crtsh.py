import requests

from utils import normalize_host

def crtsh_lookup(domain):
    url=f"https://crt.sh/?q=%25.{domain}&output=json"   
    response = requests.get(url, timeout=(10,60))

    if response.status_code != 200:
        return set()
    
    data = response.json()
    
    hosts = set()
    
    for entry in data:
        name = entry.get("name_value", "")
        for subdomain in name.split("\n"):
            host = normalize_host(subdomain)
            hosts.add(host)
    
    return hosts