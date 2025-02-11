import socket
import concurrent.futures

class PortScanner:
    def __init__(self,target_ip,start_port=1,end_port=1024):
        """initialize port scanner with target IP and port range

        Args:
            target_ip : IP address to scan
            start_port (int, optional): starting port number (default=1).
            end_port (int, optional): ending port number (default=1024).
        """
        
        self.target_ip = target_ip
        self.start_port = start_port
        self.end_port = end_port
        
    def check_port(self,port):
        """
        check if a specific port is open

        Args:
            port : port number to check
        Return:
            Port number if open, None is closed
        """
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(1) #1-second timeout
            result = sock.connect_ex((self.target_ip,port))
            sock.close()
            
            #port is considered open if connection is successful (result == 0)
            return port if result == 0 else None
        except Exception :
            return None
    
    def scan(self, max_threads=100):
        """
        scan all ports in the specified range

        Args:
            max_threads (int, optional): maximum number of concurrent threads. Defaults to 100.
        Return:
            List of open parameters
        """
        
        open_ports = []
         # use threadPoolExecutor for concurrent scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            #create future for port checking
            futures = [executor.submit(self.check_port, port) for port in range(self.start_port,self.end_port+1)]
            
            #collect results
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)

        return sorted(open_ports)
    
    
def main():
    try:
        #get target ip from the user
        target_ip = input("Enter target ip address: ")
        
        #create and run port scanner
        scanner = PortScanner(target_ip)
        open_ports = scanner.scan()
        
        #display results
        if open_ports:
            print("\nOpen Ports: ")
            for port in open_ports:
                print(f"Port {port} is open")
        else:
            print("\n No open ports found")
    except KeyboardInterrupt:
        print("\nScanning interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
if __name__=="__main__":
    main()