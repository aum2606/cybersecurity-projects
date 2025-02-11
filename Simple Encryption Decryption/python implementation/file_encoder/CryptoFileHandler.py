from file_encoder import AESCipher


class CryptoFileHandler:
    """Handles file encryption/decryption operations"""
    HEADER_SALT_LENGHT=16
    HEADER_IV_LENGTH = 12
    TAG_LENGTH = 16
    
    def __init__(self,input_path:str,output_path:str):
        self.input_path = input_path
        self.output_path = output_path
        
    def _read_encrypted_header(self) -> tuple[bytes,bytes,bytes]:
        """Read salt, IV, and tag from encrypted file"""
        with open(self.input_path,'rb') as f:
            salt = f.read(self.HEADER_SALT_LENGHT)
            iv = f.read(self.HEADER_IV_LENGTH)
            data = f.read()
            cipherText = data[:-self.TAG_LENGTH]
            tag = data[-self.TAG_LENGTH:]
        return salt, iv, tag,cipherText
    
    def encrypt(self,cipher:AESCipher)->None:
        """Encrypt file with AES-GCM"""
        encryptor = cipher.create_encryptor()
        with open(self.input_path,'rb') as f_in, \
            open(self.output_path,'wb') as f_out:
                
            # Write header(salt+IV)
            f_out.write(cipher.salt)
            f_out.write(cipher.iv)
            
            #Encrypt and write data in chunks
            while True:
                chunk = f_in.read(4096)
                if not chunk:
                    break
                f_out.write(encryptor.update(chunk))
                
            #finalize encryption and write tag
            f_out.write(encryptor.finalize())
            f_out.write(encryptor.tag)
                
    def decrypt(self,cipher: AESCipher) ->None:
        """Decrypt file with AES-GCM"""
        salt,iv,tag,ciphertext = self._read_encrypted_header()
        cipher.salt = salt
        decryptor = cipher.create_decryptor(iv,tag)
        
        with open(self.output_path,'wb') as f_out:
            f_out.write(decryptor.update(ciphertext))
            f_out.write(decryptor.finalize())
    