import nmap

def stealth_nmap_scan(target, ports='1-1024'):
    scanner = nmap.PortScanner()

    try:
        print(f"\n[+] Stealth scanning {target} on ports {ports}...\n")
        # Stealthy arguments
        stealth_args = (
            f"-sS -T1 -Pn --data-length 50 --spoof-mac 0 "
            f"-p {ports}"
        )

        scanner.scan(hosts=target, arguments=stealth_args)

        for host in scanner.all_hosts():
            print(f"Host: {host} ({scanner[host].hostname()})")
            print(f"State: {scanner[host].state()}")

            for proto in scanner[host].all_protocols():
                print(f"\nProtocol: {proto}")
                ports_list = scanner[host][proto].keys()
                for port in sorted(ports_list):
                    state = scanner[host][proto][port]['state']
                    name = scanner[host][proto][port].get('name', 'unknown')
                    print(f"Port: {port}\tState: {state}\tService: {name}")
    except Exception as e:
        print(f"Error during scan: {e}")

# Usage
if __name__ == "__main__":
    target_ip = input("Enter target IP/domain: ").strip()
    port_range = input("Enter port range (default 1-1024): ").strip() or "1-1024"
    stealth_nmap_scan(target_ip, port_range)
