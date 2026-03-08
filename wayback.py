import requests
import json
from urllib.parse import urlparse

from utils import normalize_host

def get_wayback_urls(domain):
    url = "http://web.archive.org/cdx/search/cdx"
    
    params = {
        "url": f"*.{domain}",
        "output": "json",
        "fl": "original",
        "collapse": "urlkey"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return set()

    data = response.json()
    
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    hosts = set()

    # Saltamos la cabecera
    for row in data[1:]:
        url = row[0]

        parsed = urlparse(url)
        host = parsed.netloc.lower()
        host = normalize_host(host)
        
        hosts.add(host)
    
    return hosts