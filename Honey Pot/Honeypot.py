import socket 
import threading
import datetime
import logging

#logging configuration
logging.basicConfig(filename='Honeypot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Honeypot:
    def __init__(self,host='0.0.0.0',port=2222):
        self.host=  host
        self.port = port
        self.server_socket = None

    def start(self):
        """start honey pot server"""
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind(self.host,self.port)
        self.server_socket.listen(5)

        print(f"[+] Honeypot listening on {self.host} : {self.port}")

        while True:
            client,address = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_connection,args=(client,address))
            client_handler.start()

    def handle_connection(self,client_socket,address):
        """handle incoming connection"""
        print(f"[*] Incoming connection from {address[0]} : {address[1]}")
        logging.info(f"New connection from {address[0]} : {address[1]}")

        #send fake SSH banner
        client_socket.send(b"SSH-2.0-OpenSSH_7.2p1 Ubuntu-4ubuntu2.8\n")

        try:
            #collect login attempts
            clien_socket.send(b"Login as: ")
            username = client_socket.recv(1024).decode().strip()

            client_socket.send(b"password: ")
            password = client_socket.recv(1024).decode().strip()

            #log the attempted credentials
            logging.info(
                f"Login attempt: - IP : {address[0]} : {address[1]}"
                f"Username: {username} Password: {password}"
            )

            #simulate failed login
            client_socket.send(b"Access denied\n")
        except Exception as e:
            logging.error(f"Error handling connection: {str(e)}")
        finally:
            client_socket.close()


def main():
    try:
        honeypot = Honeypot()
        honeypot.start()
    except KeyboardInterrupt:
        print(f"\n[!] Shutting down honeypot....")
    except Exception as e:
        print(f"[!] Error: {str(e)}")


if __name__ == "__main__":
    main()