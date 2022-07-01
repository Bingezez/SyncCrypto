from os.path import join
from random import randint
from sympy import randprime
from lib.utils import hash_string_sha224


def random_prime():
    return randprime(0, 2 ** 16)


def random_number():
    return randint(0, 2 ** 16)


class DiffieHellman:
    def __init__(self):
        self.pub_key1 = None
        self.pub_key2 = None
        self._prv_key = None
        self._full_key = None
        self.trans_channel = None

        self.encrypted_message = ''
        self.decrypted_message = ''

    def __aenter__(self):
        return self

    def prv_key(self, key):
        self._prv_key = key

    async def save_key(self, path='./'):
        async with open(join(path, 'pub_key1'), 'w') as f:
            await f.write(str(self.pub_key1))
        async with open(join(path, 'pub_key2'), 'w') as f:
            await f.write(str(self.pub_key2))
        async with open(join(path, 'prv_key'), 'w') as f:
            await f.write(str(self._prv_key))

    async def save_full_key(self, path='./'):
        async with open(join(path, 'full_key'), 'w') as f:
            await f.write(str(self._full_key))

    def load_key(self, path='./'):
        self.pub_key1 = int(open(join(path, 'pub_key1')).read())
        self.pub_key2 = int(open(join(path, 'pub_key2')).read())
        self._prv_key = int(open(join(path, 'prv_key')).read())

    def load_full_key(self, path='./'):
        self._full_key = int(open(join(path, 'full_key')).read())

    def generate_partial_key(self):
        self.trans_channel = pow(self.pub_key1, self._prv_key, self.pub_key2)

    def generate_full_key(self, partial_key_r):
        self._full_key = pow(partial_key_r, self._prv_key, self.pub_key2)

    def encrypt_message(self, message):
        for c in message:
            encrypted_message += chr(ord(c) + self._full_key)

    def decrypt_message(self, encrypted_message):
        for c in encrypted_message:
            decrypted_message += chr(ord(c) - self._full_key)


if __name__ == '__main__':
    m = random_prime()
    n = random_prime()
    alice = DiffieHellman()
    alice.pub_key1 = m
    alice.pub_key2 = n
    alice.prv_key(random_number())
    alice.generate_partial_key()

    bob = DiffieHellman()
    bob.pub_key1 = m
    bob.pub_key2 = n
    bob.prv_key(random_number())
    bob.generate_partial_key()

    print(f'Оpen data channel [Alice: {alice.trans_channel}, Bob: {bob.trans_channel}]')
    alice.generate_full_key(bob.trans_channel)
    bob.generate_full_key(alice.trans_channel)

    print(hash_string_sha224('Hello!!'))
    enc_alice = alice.encrypt_message(hash_string_sha224('Hello!!'))
    print(f'Encrypt message {enc_alice}')
    dec_bob = bob.decrypt_message(enc_alice)

    print(f'Decrypt message {dec_bob}')
