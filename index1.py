import nmap

def nmap_scan(target, ports='1-1024'):
    scanner = nmap.PortScanner()

    try:
        print(f"\nScanning {target} on ports {ports}...")
        scanner.scan(hosts=target, arguments=f'-p {ports} -T4 -sV')

        for host in scanner.all_hosts():
            print(f"\nHost: {host} ({scanner[host].hostname()})")
            print(f"State: {scanner[host].state()}")

            for protocol in scanner[host].all_protocols():
                print(f"\nProtocol: {protocol}")
                ports_list = scanner[host][protocol].keys()
                for port in sorted(ports_list):
                    state = scanner[host][protocol][port]['state']
                    name = scanner[host][protocol][port].get('name', 'unknown')
                    print(f"Port: {port}\tState: {state}\tService: {name}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    target_input = input("Enter target IP or domain (e.g. 192.168.1.1 or scanme.nmap.org): ")
    port_range = input("Enter port range (e.g. 1-1000) [Press Enter for default 1-1024]: ") or '1-1024'
    nmap_scan(target_input.strip(), port_range.strip())
