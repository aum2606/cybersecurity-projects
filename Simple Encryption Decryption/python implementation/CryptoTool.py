from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoTool:
    def __init__(self):
        self.salt = os.urandom(16)
        self.fernet = None
        
    def generate_key(self,password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)
        
    def encrypt(self,message,password):
        self.generate_key(password)
        encrypted_message = self.fernet.encrypt(message.encode())
        return {
            'salt' : base64.b64encode(self.salt).decode('utf-8'),
            'message': base64.b64encode(encrypted_message).decode('utf-8')
        }
    
    def decrypt(self,encrypted_data,password):
        self.salt = base64.b64decode(encrypted_data['salt'])
        self.generate_key(password)
        decrypted_message = self.fernet.decrypt(base64.b64decode(encrypted_data['message']))
        return decrypted_message.decode()


def main():
    crypto = CryptoTool()
    
    while True:
        print("\n Encryption/Decryption Tool")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '3':
            break
        
        if choice == '1':
            message = input("Enter message to encrypt: ")
            password = input("Enter password: ")
            
            try:
                encrypted_data = crypto.encrypt(message,password)
                print("\nEncrypted data: ")
                print(f"Salt: {encrypted_data['salt']}")
                print(f"Encrypted message: {encrypted_data['message']}")
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == '2':
            try:
                salt = input("inner salt: ")
                encrypted_message = input("Enter encrypted message: ")
                password = input("Enter password: ")
                encrypted_data = {
                    'salt' : salt,
                    'message': encrypted_message
                }
                decrypted_message = crypto.decrypt(encrypted_data,password)
                print(f"\nDecrypted message: {decrypted_message}")
            except Exception as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice. Please choose a valid option.")
            
            
if __name__ == "__main__":
    main()