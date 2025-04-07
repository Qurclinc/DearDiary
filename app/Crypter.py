import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class Crypter:

    def __init__(self):
        self.MODE = AES.MODE_CBC
        self.BLOCK_SIZE = 16

    def __generate_key(self, key):
        if len(key) < 16: key += "0" * (16 - len(key))
        else: key = key[:16]
        return key.encode("utf-8")
    
    def encrypt(self, text, key):
        try:
            iv = get_random_bytes(self.BLOCK_SIZE)
            cipher = AES.new(self.__generate_key(key), self.MODE, iv)
            encrypted_data = base64.b64encode(iv + cipher.encrypt(pad(text.encode("utf-8"), AES.block_size)))
            return encrypted_data.decode("utf-8")
        except Exception:
            raise "Encryption error"
    
    def decrypt(self, text, key):
        try:
            iv = base64.b64decode(text)[:AES.block_size]
            cipher = AES.new(self.__generate_key(key), self.MODE, iv)
            text = base64.b64decode(text)[AES.block_size:]
            decrypted_data = unpad(cipher.decrypt(text), AES.block_size)
            return decrypted_data.decode("utf-8")
        except Exception:
            raise "Decryption error"


