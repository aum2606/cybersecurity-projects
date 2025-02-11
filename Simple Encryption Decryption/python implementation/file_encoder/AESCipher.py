import os
from typing import Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AESCipher:
    """AES-GCM encryption/decryption handler"""
    def __init__(self, password: str, salt: Optional[bytes] = None):
        self.password = password.encode()
        self.salt = salt if salt else os.urandom(16)
        self.key = self._derive_key()
        self.iv: Optional[bytes] = None
        self.tag: Optional[bytes] = None
        
    def _derive_key(self)->bytes:
        """Derive encryption key using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.password)

    def create_encryptor(self) -> Cipher:
        """Create AES-GCM encryptor with random IV"""
        self.iv = os.urandom(12)
        return Cipher(
            algorithms.AES(self.key),
            modes.GCM(self.iv),
            backend=default_backend()
        ).encryptor()
        
    def create_decryptor(self,iv:bytes,tag:bytes) -> Cipher:
        """Generate AES-GCM decryptor with provided IV and tag"""
        self.iv = iv
        self.tag = tag
        return Cipher(
            algorithms.AES(self.key),
            modes.GCM(self.iv, self.tag),
            backend=default_backend()
        ).decryptor()