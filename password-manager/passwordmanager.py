from ast import Pass
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import json
import base64
import os


class PasswordManager:
    def __init__(self,master_password):
        self.salt = get_random_bytes(32)
        self.key = PBKDF2(master_password, self.salt, dklen=32,count=1000000)
        self.passwords_file = 'passwords.enc'
        self.passwords = {}
        self.load_passwords()

    def _encrypt(self,data):
        iv = get_random_bytes(16)
        cipher = AES.new(self.key,AES.MODE_CBC,iv)
        encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(iv + encrypted_data).decode('utf-8')

    def _decrypt(self,encrypted_data):
        try:
            raw = base64.b64decode(encrypted_data.encode('utf-8'))
            iv = raw[:16]
            encrypted_text = raw[16:]
            cipher = AES.new(self.key,AES.MODE_CBC,iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_text),AES.block_size)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            print(f"Error decrypting data: {e}")
            return None

    def _save_passwords(self):
        encrypted_data = self._encrypt(json.dumps(self.passwords))
        with open(self.passwords_file,'w') as f:
            json.dump({
                'salt': base64.b64encode(self.salt).decode('utf-8'),
                'passwords': encrypted_data
            },f)
    
    def _load_passwords(self):
        if os.path.exists(self.passwords_file):
            try:
                    
                with open(self.passwords_file,'r') as f:
                    data = json.load(f)
                    self.salt = base64.b64decode(data['salt'].encode('utf-8'))
                    decrypted_data = self._decrypt(data['data'])
                    if decrypted_data:
                        self.passwords = json.loads(decrypted_data)
            except Exception as e:
                print(f"Error loading passwords: {e}")

    def add_password(self,service,username,password):
        """add or update a password for a service"""
        self.passwords[service] = {
            'username':username,
            'password':password
        }
        self._save_passwords()

    def get_password(self,service):
        """Retrieve password for a service"""
        return self.passwords.get(service)

    def delete_password(self,service):
        """Delete password for a service"""
        if service in self.passwords:
            del self.passwords[service]
            self._save_passwords()
            return True
        return False

    def list_services(self):
        """List all stored servies"""
        return list(self.passwords.keys())
            

#Example usage
if __name__ == "__main__":
    #create a password manager instance with a master password 
    master_password = input("Enter master password: ")
    pm = PasswordManager(master_password)

    while True:
        print("\nPassword Manager Menu:  ")
        print("1. Add/Update Password")
        print("2. Get Password")
        print("3. Delete Password")
        print("4. List Services")
        print("5. Exit")

        choice = input("Enter your choice: (1-5) ")
        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            pm.add_password(servie,username,password)
            print("Password saved successfully!")

        elif chocie == '2':
            service = input("Enter service name: ")
            credentials = pm.get_password(service)
            if credentials:
                print(f"\nUsername: {credentials['username']}")
                print(f"Password: {credentials['password']}")
            else:
                print("Service not found!")

        elif choice == '3':
            service = input("Enter servie name: ")
            if pm.delete_password(service):
                print("Password deleted successfully!")
            else:
                print("Service not found!")

        elif choice == '4':
            services = pm.list_services()
            if services:
                print("\n Stored servies: ")
                for service in services:
                    print(F"- {service}")
            else:
                print("No passwords stored yet!")

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again!")