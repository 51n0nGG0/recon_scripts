import dns.resolver

def host_inspection(host):
    record_types = ["A", "AAAA", "CNAME", "MX", "NS"]

    results = {}
    ips = []
    domains = []

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(host, rtype)

            if rtype in ["A", "AAAA"]:
                values = [r.to_text() for r in answers]
                ips.extend(values)
                results[rtype] = {"ips": values}

            elif rtype == "CNAME":
                target = answers[0].target.to_text().rstrip(".")
                domains.append(target)
                results[rtype] = {"domain": target}

            elif rtype == "MX":
                targets = [r.exchange.to_text().rstrip(".") for r in answers]
                domains.extend(targets)
                results[rtype] = {"domain": targets}

            elif rtype == "NS":
                targets = [r.target.to_text().rstrip(".") for r in answers]
                domains.extend(targets)
                results[rtype] = {"domain": targets}

        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            print (f"[\033[31mINACTIVE\033[0m] {host}")
            return {"status": "INACTIVE", "ips": [], "domains": [], "records": {}}
        except Exception:
            continue
    if results:
        print(f"[\033[32mACTIVE\033[0m] {host}")
        
        print("  Records:")
        for rtype, data in results.items():
            print(f"    {rtype}: {data}")
            
        print(f"  IPs: {', '.join(set(ips))}")
        print(f"  Domains: {', '.join(set(domains))}")
        
        return {
            "status": "ACTIVE",
            "ips": list(set(ips)),
            "domains": list(set(domains)),
            "records": results
        }
    else:
        print(f"[\033[33mNO ANSWER\033[0m] {host}")
        return {"status": "NO ANSWER", "ips": [], "domains": [], "records": {}}