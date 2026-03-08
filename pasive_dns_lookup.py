import questionary

from datetime import datetime

from crtsh import crtsh_lookup
from exporter import save_data_to_csv
from wayback import get_wayback_urls
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
            "Manual Selection (Not Yet Developed)",
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
        save_data_to_csv(target_domain, results)
    
    elif main_menu_choice == "Manual Selection":
        print("Not yet developed. Exiting...")
        exit(0)
                
                
            
    