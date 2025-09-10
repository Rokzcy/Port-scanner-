use std::net::{TcpStream, SocketAddr};
use std::thread;
use std::time::Duration;

struct PortScanner {
    target_host: String,
    start_port: u16,
    end_port: u16,
}

impl PortScanner {
    fn new(target_host: &str, start_port: u16, end_port: u16) -> Self {
        PortScanner {
            target_host: target_host.to_string(),
            start_port,
            end_port,
        }
    }

    // Check if a port is open
    fn is_port_open(&self, port: u16) -> bool {
        let addr = format!("{}:{}", self.target_host, port);
        let socket_addr: SocketAddr = addr.parse().unwrap();

        match TcpStream::connect_timeout(&socket_addr, Duration::from_secs(1)) {
            Ok(_) => true,
            Err(_) => false,
        }
    }

    // Scan one port
    fn scan_port(&self, port: u16) {
        if self.is_port_open(port) {
            println!("[+] Port {} is OPEN", port);
        }
    }

    // Run scanner with threads
    fn run(&self) {
        println!(
            "[*] Starting scan on {} from {} to {}...\n",
            self.target_host, self.start_port, self.end_port
        );

        let mut handles = vec![];

        for port in self.start_port..=self.end_port {
            let host_clone = self.target_host.clone();
            let handle = thread::spawn(move || {
                let scanner = PortScanner::new(&host_clone, port, port);
                scanner.scan_port(port);
            });
            handles.push(handle);
        }

        for handle in handles {
            let _ = handle.join();
        }

        println!("\n[*] Scan complete.");
    }
}

fn main() {
    let target = "127.0.0.1"; // Change to your target IP
    let scanner = PortScanner::new(target, 1, 1024);
    scanner.run();
          }
