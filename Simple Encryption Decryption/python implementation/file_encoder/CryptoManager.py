import argparse
import os
from file_encoder import AESCipher, CryptoFileHandler


class CryptoManager:
    """Main encryption/decryption workflow manager"""
    def __init__(self,mode:str,input_path:str,out_path:str,password:str):
        self.mode = mode
        self.input_path = input_path
        self.out_path = out_path
        self.password = password
        
    def execute(self) ->None:
        """Execute the requested operation"""
        if self.mode == 'encrypt':
            cipher = AESCipher(self.password)
            handler = CryptoFileHandler(self.input_path,self.output_path)
            handler.encrypt(cipher)
        elif self.mode == 'decrypt':
            handler = CryptoFileHandler(self.password)
            cipher = AESCipher(self.password,salt=os.urandom(16))
            handler.decrypt(cipher)
        else:
            raise ValueError("Invalid mode. Please use 'encrypt' or 'decrypt'")
        


def main():
    parser = argparse.ArgumentParser(description='File Encryption tool')
    parser.add_argument("mode",choices=['encrypt','decrypt'],help='Operation mode')
    parser.add_argument("input",help='Input file path')
    parser.add_argument('output',help='Output file path')
    parser.add_argument('-p','--password',required=True,help='Encryption password')
    
    args = parser.parse_args()
    
    try: 
        manager = CryptoManager(args.mode,args.input,args.output,args.password)
        manager.execute()
        print("Operation completed successfull")
    except Exception as e:
        print(f"Error: {str(e)}")
        
if __name__ == "__main__":
    main()
    