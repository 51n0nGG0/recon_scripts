import requests
import dns.resolver
import json

from datetime import datetime
from urllib.parse import urlparse

def normalize_host(host):
    host = host.lower().strip()
        
    if host.startswith("*."):
        host = host[2:]
        
    if host.startswith("www."):
        host = host[4:]

    return host

def dns_inspection(host):
    try:
        answers = dns.resolver.resolve(host, "A")
        ips = [rdata.to_text() for rdata in answers]
        print(f"[\033[32mACTIVE\033[0m] {host} - IPs: {', '.join(ips)}]")
        return {"status": "ACTIVE", "ips": ips} 
    except dns.resolver.NXDOMAIN:
        print(f"[\033[31mINACTIVE\033[0m] {host}")
        return {"status": "INACTIVE", "ips": []}
    except dns.resolver.NoAnswer:
        print(f"[\033[33mNO ANSWER\033[0m] {host}")
        return {"status": "NO ANSWER", "ips": []}
    except Exception:
        return {"status": "ERROR", "ips": []}

def extract_hosts(urls):
    hosts = set()
    
    for url in urls:
        try:
            parsed = urlparse(url)
            host = parsed.netloc.lower()
            
            if host:
                hosts.add(host)
        except Exception:
            pass
    
    return hosts

def crtsh_lookup(domain):
    url=f"https://crt.sh/?q=%25.{domain}&output=json"   
    response = requests.get(url, timeout=(10,60))

    if response.status_code != 200:
        return
    
    data = response.json()
    
    hosts = set()
    
    for entry in data:
        name = entry.get("name_value", "")
        for subdomain in name.split("\n"):
            host = normalize_host(subdomain)
            hosts.add(host)
    
    return hosts


def pasive_dns_lookup(domain):
    results = []
    
    print("[\033[34mINF\033[0m] Extracting subdomains from crt.sh...")
    hosts = crtsh_lookup(domain)
    
    print(f"[\033[34mINF\033[0m] Found {len(hosts)} unique hosts. Performing DNS inspection...")
    for host in hosts:
        dns_result = dns_inspection(host)
        results.append({"host": host, "dns_tatus": dns_result["status"], "ips": dns_result["ips"]})    
    return results

def save_to_json(domain, data):
    filename = f"{domain}_recon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    output = {
        "target": domain,
        "total_hosts": len(data),
        "generated_at": datetime.now().isoformat(),
        "results": data
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"[\033[34mINF\033[0m] Results saved to {filename}")
        
if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., example.com): ")
    results = pasive_dns_lookup(target_domain)
    save_to_json(target_domain, results)
    