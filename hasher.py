from Crypto.Hash import SHAKE128


class Hasher:
    def __init__(self, key1, key2):
        self.key1 = key1
        self.key2 = key2

    def generate(self):
        key = self.key1 + self.key2
        shake = SHAKE128.new()
        shake.update(key.encode())
        key = shake.read(16)
        return key
