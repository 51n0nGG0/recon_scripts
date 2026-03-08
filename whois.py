from ipwhois import IPWhois
    
def whois_lookup(ip):
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap()
        
        # Información base
        output = {
            "asn": res.get("asn"),
            "asn_description": res.get("asn_description"),
            "country": res.get("asn_country_code"),
            "network": res.get("network", {}).get("name"),
            "cidr": res.get("network", {}).get("cidr"),
            "contacts": []
        }

        # Extraer contactos desde entities
        for entity in res.get("objects", {}).values():
            contact = entity.get("contact")
            if not contact:
                continue

            # Solo personas físicas o contactos individuales
            if contact.get("kind") != "individual":
                continue

            output["contacts"].append({
                "name": contact.get("name"),
                "email": contact.get("email"),
                "address": contact.get("address"),
                "phone": contact.get("phone"),
                "roles": entity.get("roles")
            })

        print(f"[\033[36mWHOIS\033[0m] {ip} - ASN: {output['asn']} | Country: {output['country']} | Network: {output['network']} | CIDR: {output['cidr']}")
        
        return output

    except Exception as e:
        return {"error": str(e)}