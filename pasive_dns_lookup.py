import ipaddress
import questionary

from datetime import datetime

from crtsh import crtsh_lookup
from exporter import save_data_to_json, save_data_to_csv
from wayback import get_wayback_urls
from whois import whois_lookup
from host_inspection import host_inspection

def pasive_dns_lookup(domain):
    results = []
    
    print("[\033[34mINF\033[0m] Extracting subdomains from crt.sh...")
    crtsh_hosts = crtsh_lookup(domain)
    
    print("[\033[34mINF\033[0m] Extracting subdomains from Wayback Machine...")
    wayback_hosts = get_wayback_urls(domain)
    
    hosts = crtsh_hosts | wayback_hosts
    
    print(f"[\033[34mINF\033[0m] Found {len(hosts)} unique hosts. Performing DNS inspection...")
    for host in hosts:
        host_inspection_results = host_inspection(host)
        
        """
        ips_info = []

        for ip in host_inspection_results["ips"]:
            ip_data = {"ip": ip}

            if ipaddress.ip_address(ip).is_private:
                print(f"[\033[33mSKIP\033[0m] {host} - IP {ip} is private, skipping WHOIS lookup.")
                ip_data["whois"] = None
            else:
                ip_data["whois"] = whois_lookup(ip)

            ips_info.append(ip_data)
        """
        
        results.append({
            "host": host,
            **host_inspection_results
        })
        
    return results
        
if __name__ == "__main__":
    
    print("""
██████╗  █████╗ ███████╗    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝███████║███████╗    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔═══╝ ██╔══██║╚════██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║     ██║  ██║███████║    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝     ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
    """)
    
    print(f"[+] Version: 1.0")
    print(f"[+] Author: Eloy Alfredo Schmidt Rodríguez")
    print(f"[+] Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    main_menu_choice = questionary.rawselect(
        "Select an option:",
        choices=[
            "Full Automatic Analysis",
            "Manual Selection",
            "Exit"
        ],qmark="",
        pointer="❯"
    ).ask()
    
    if main_menu_choice == "Exit":
        print("Exiting...")
        exit(0)

    if main_menu_choice == ("Full Automatic Analysis"):
        target_domain = input("Enter the target domain (e.g., example.com): ")
        results = pasive_dns_lookup(target_domain)
        save_data_to_json(target_domain, results)
    
    elif main_menu_choice == "Manual Selection":
        manual_menu_selected_modules = questionary.checkbox(
            "Select modules to execute:",
            choices=[
                "Subdomain Enumeration",
                "DNS Inspection",
                "WHOIS Lookup"
            ],qmark="",
            pointer="❯"
        ).ask()

        if not manual_menu_selected_modules:
            print("No modules selected.")
            exit(0)
            
        if "Subdomain Enumeration" in manual_menu_selected_modules:
            while True:
                subdomain_menu_selected_modules = questionary.checkbox(
                    "Select subdomain enumeration sources:",
                    choices=[
                        "crt.sh",
                        "Wayback Machine"
                    ],qmark="",
                    pointer="❯"
                ).ask()
                
                if not subdomain_menu_selected_modules:
                    print(" You must select at least one source.")
                else:
                    break
            
            scope_menu_choice = questionary.rawselect(
                "Select scope for subdomain enumeration:",
                choices=[
                    "Target Domain Only",
                    "Include Subdomains"
                ],qmark="",
                pointer="❯"
            ).ask()
                
                
            
    