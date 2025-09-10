import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

public class PortScanner {
    private String targetHost;
    private int startPort;
    private int endPort;

    public PortScanner(String targetHost, int startPort, int endPort) {
        this.targetHost = targetHost;
        this.startPort = startPort;
        this.endPort = endPort;
    }

    // Check if port is open
    public boolean isPortOpen(String host, int port, int timeout) {
        try (Socket socket = new Socket()) {
            socket.connect(new InetSocketAddress(host, port), timeout);
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    // Scan single port
    public void scanPort(int port) {
        if (isPortOpen(targetHost, port, 1000)) {
            System.out.println("[+] Port " + port + " is OPEN");
        }
    }

    // Run the scanner
    public void run() {
        System.out.println("[*] Starting scan on " + targetHost + " from port " + startPort + " to " + endPort + "...\n");

        for (int port = startPort; port <= endPort; port++) {
            final int p = port;
            Thread thread = new Thread(() -> scanPort(p));
            thread.start();
        }
    }

    // Main method
    public static void main(String[] args) {
        String target = "127.0.0.1"; // Change to your target IP
        int start = 1;
        int end = 1024;

        PortScanner scanner = new PortScanner(target, start, end);
        scanner.run();
    }
}
