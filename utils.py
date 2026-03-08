from urllib.parse import urlparse

def normalize_host(host):
    host = host.lower().strip()
        
    if host.startswith("*."):
        host = host[2:]
        
    if host.startswith("www."):
        host = host[4:]

    if host.endswith("."):
        host = host[:-1]
        
    if ":" in host:
        host = host.split(":", 1)[0]
        
    return host

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