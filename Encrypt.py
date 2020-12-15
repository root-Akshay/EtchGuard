from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from hasher import Hasher
import os

class Encryt(Hasher):
    def __init__(self, key1, key2):
        super().__init__(key1, key2)

    def encrypt(self, mess):
        cipher = AES.new(self.generate(), AES.MODE_GCM)
        e1, t1 = cipher.encrypt_and_digest(mess)
        return e1, t1, cipher.nonce

    def encrypt_vault(self,name,namedb):
        name=f"vaults/{name}"
        namedb=f"vaults/{namedb}"
        with open(namedb, "rb") as foo:
            pt = foo.read()
        enc, tag, nonce = self.encrypt(pt)
        with open(name + ".enc", "wb") as bar:
            bar.write(b64encode(enc) + b" " + b64encode(tag) + b" " + b64encode(nonce))
        os.remove(namedb)


""" d = Encryt("tempmail@gmail.com", "masterpassword")
d.encrypt_vault() """ 
