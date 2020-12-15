from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from hasher import Hasher


class Decrypt(Hasher):
    def __init__(self, key1, key2):
        super().__init__(key1, key2)

    def decrypt_vault(self,nameenc,namedb):
        nameenc=f"vaults/{nameenc}"
        namedb=f"vaults/{namedb}"
        with open(nameenc, "rb") as foo:
            ciphertext = foo.read()
        self.ciphertext = ciphertext.split(b" ")
        dec = self.decrypt(b64decode(self.ciphertext[0]), b64decode(self.ciphertext[1]))
        with open(namedb, "wb") as foo:
            foo.write(dec)
        #print("done")

    def decrypt(self, ct, tag):
        cipher = AES.new(self.generate(), AES.MODE_GCM, b64decode(self.ciphertext[2]))
        e1 = cipher.decrypt_and_verify(ct, tag)
        return e1

""" 
d = Decrypt("tempmail@gmail.com", "masterpassword")
d.decrypt_vault() 
 """