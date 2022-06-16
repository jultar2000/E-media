import random

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA as rsa_library


class RSA:

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def ecb_encrypt(self, data):
        key_size = self.public_key['n'].bit_length()
        encrypted_data = []
        step = key_size // 8 - 1
        for i in range(0, len(data), step):
            raw_data_bytes = bytes(data[i:i + step])
            raw_data_int = int.from_bytes(raw_data_bytes, 'big')
            encrypted_data_int = pow(raw_data_int, self.public_key['e'], self.public_key['n'])
            encrypted_data_bytes = encrypted_data_int.to_bytes(step + 1, 'big')
            for encrypted_byte in encrypted_data_bytes:
                encrypted_data.append(encrypted_byte)
        return encrypted_data

    def ecb_decrypt(self, data):
        key_size = self.private_key['n'].bit_length()
        decrypted_data = []
        step = key_size // 8

        for i in range(0, len(data), step):
            encrypted_bytes = b''
            for byte in data[i:i + step]:
                encrypted_bytes += byte.to_bytes(1, 'big')
            encrypted_data_int = int.from_bytes(encrypted_bytes, 'big')
            decrypted_data_int = pow(encrypted_data_int, self.private_key['d'], self.private_key['n'])
            decrypted_data_bytes = decrypted_data_int.to_bytes(step - 1, 'big')
            for decrypted_byte in decrypted_data_bytes:
                decrypted_data.append(decrypted_byte)
        return decrypted_data

    def cbc_encrypt(self, data):
        key_size = self.public_key['e'].bit_length()
        encrypted_data = []
        step = key_size // 8 - 1
        previous = random.getrandbits(key_size)
        print(f"First Initialization Vector: {previous}")
        for i in range(0, len(data), step):
            raw_data_bytes = bytes(data[i:i + step])

            previous = previous.to_bytes(step + 1, 'big')
            previous = int.from_bytes(previous[:len(raw_data_bytes)], 'big')
            xor = int.from_bytes(raw_data_bytes, 'big') ^ previous

            encrypted_data_int = pow(xor, self.public_key['e'], self.public_key['n'])
            previous = encrypted_data_int
            encrypted_data_bytes = encrypted_data_int.to_bytes(step + 1, 'big')

            for encrypted_byte in encrypted_data_bytes:
                encrypted_data.append(encrypted_byte)
        return encrypted_data

    def cbc_decrypt(self, data, initialization_vector):
        key_size = self.private_key['n'].bit_length()
        decrypted_data = []
        step = key_size // 8
        previous = initialization_vector

        for i in range(0, len(data), step):
            encrypted_bytes = b''
            for byte in data[i:i + step]:
                encrypted_bytes += byte.to_bytes(1, 'big')

            encrypted_data_int = int.from_bytes(encrypted_bytes, 'big')
            decrypted_data_int = pow(encrypted_data_int, self.private_key['d'], self.private_key['n'])

            previous = previous.to_bytes(step, 'big')
            previous = int.from_bytes(previous[:step - 1], 'big')
            xor = previous ^ decrypted_data_int

            decrypted_data_bytes = xor.to_bytes(step - 1, 'big')
            for decrypted_byte in decrypted_data_bytes:
                decrypted_data.append(decrypted_byte)

            previous = int.from_bytes(encrypted_bytes, 'big')
        return decrypted_data

    def crypto_library_encrypt(self, IDAT_data):
        keys_library = rsa_library.construct((self.public_key['n'], self.public_key['e']))
        encoder_library = PKCS1_OAEP.new(keys_library)
        key_size = self.public_key['n'].bit_length()
        block_size = key_size // 16 - 1
        encrypted_data = bytearray()
        after_iend_data = bytearray()

        for i in range(0, len(IDAT_data), block_size):
            bytes_block = bytes(IDAT_data[i:i + block_size])
            encrypt_block_bytes = encoder_library.encrypt(bytes_block)

            after_iend_data.append(encrypt_block_bytes[-1])
            encrypt_block_bytes = encrypt_block_bytes[:-1]
            encrypted_data += encrypt_block_bytes

        return encrypted_data, after_iend_data
