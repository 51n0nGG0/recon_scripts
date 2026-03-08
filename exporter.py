import json
import csv

from datetime import datetime

def save_data_to_csv(domain, data):
    filename = f"{domain}_recon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        writer.writerow(["host", "status", "record_type", "address"])
        
        for entry in data:
            host = entry.get("host", "")
            status = entry.get("status", "")
            records = entry.get("records", {})

            if not records:
                writer.writerow([host, status, "", ""])
            else:
                for record_type, record_data in records.items():

                    addresses = []

                    if "ips" in record_data:
                        addresses = record_data["ips"]

                    elif "domain" in record_data:
                        if isinstance(record_data["domain"], list):
                            addresses = record_data["domain"]
                        else:
                            addresses = [record_data["domain"]]

                    for addr in addresses:
                        writer.writerow([
                            host,
                            status,
                            record_type,
                            addr
                        ])

def save_data_to_json(domain, data):
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