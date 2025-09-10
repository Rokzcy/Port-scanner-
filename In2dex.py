import socket
import threading
import time

# Class Definition
class PortScanner:
    def __init__(self, target_host, start_port, end_port):
        self.target_host = target_host
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []

    # is_port_open Method
    def is_port_open(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((self.target_host, port))
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    # scan_port Method
    def scan_port(self, port):
        if self.is_port_open(port):
            print(f"[+] Port {port} is OPEN")
            self.open_ports.append(port)

    # run Method
    def run(self):
        print(f"[*] Starting scan on {self.target_host} from {self.start_port} to {self.end_port}...\n")
        threads = []

        for port in range(self.start_port, self.end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("\n[*] Scan complete.")
        if self.open_ports:
            print(f"Open ports: {self.open_ports}")
        else:
            print("No open ports found.")

# Example usage
if __name__ == "__main__":
    target = "127.0.0.1"    # Change to target IP/hostname
    scanner = PortScanner(target, 1, 1024)
    scanner.run()
