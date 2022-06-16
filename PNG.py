import zlib

from matplotlib import image as mpimg, pyplot as plt
from Chunk import *
import numpy as np
import cv2

from Keys import Keys
from rsa import RSA


class PNG:
    def __init__(self, path):
        try:
            self.file = open(path, 'rb')
        except IOError as e:
            raise e
        self.PNG_MAGIC_NUMBER = b'\x89PNG\r\n\x1a\n'
        if self.file.read(8) != self.PNG_MAGIC_NUMBER:
            raise Exception('This file is not a PNG')
        self.chunks = []
        self.encrypt_data = bytearray()
        self.decrypt_data = bytearray()
        self.encrypt_data_from_library = bytearray()

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def display_file(self):
        tmp_png = self.file
        tmp_png.seek(0)
        img = mpimg.imread(tmp_png)
        plt.imshow(img)
        plt.show()
        tmp_png.seek(8)

    def display_original_and_cleaned_file(self, path, file_name):
        file_path = 'images/' + file_name + '.png'
        img = mpimg.imread(path)
        self.create_file_only_with_critical_chunks(file_path)
        img2 = mpimg.imread(file_path)

        plt.subplot(121), plt.imshow(img)
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img2)
        plt.title('Cleaned Image'), plt.xticks([]), plt.yticks([])
        plt.show()

    def fourier_transform(self, path):
        img = cv2.imread(path, 0)
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))
        phase_spectrum = np.asarray(np.angle(fshift))

        plt.subplot(221), plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(phase_spectrum, cmap='gray')
        plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])

        plt.subplot(223), plt.imshow(img, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        inverted_f = np.fft.ifft2(f)
        plt.subplot(224), plt.imshow(np.abs(inverted_f), cmap='gray')
        plt.title('Inverted Fourier'), plt.xticks([]), plt.yticks([])

        plt.show()

    def display_file_in_hex(self):
        content = [hex(x) for x in self.file.read()]
        print(content[0:1000])

    def print_chunks(self):
        for chunk in self.chunks:
            chunk.__str__()

    def clear_chunks(self):
        self.file.seek(8)
        self.chunks.clear()

    def read_all_chunks(self):
        self.chunks = []
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            data = self.file.read(int.from_bytes(length, 'big'))
            crc = self.file.read(Chunk.CRC_FIELD_LEN)
            specific_chunk = CHUNKTYPES.get(type_, Chunk)
            chunk = specific_chunk(length, data, type_, crc)
            self.chunks.append(chunk)
            if type_ == b'IEND':
                self.file.seek(8)
                break

    def encrypt_chunks(self, oper_type):
        self.chunks = []
        keys = Keys(512)
        public_key = keys.generate_public_key()
        private_key = keys.generate_private_key()
        rsa = RSA(public_key, private_key)
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            data = self.file.read(int.from_bytes(length, 'big'))
            crc = self.file.read(Chunk.CRC_FIELD_LEN)
            specific_chunk = CHUNKTYPES.get(type_, Chunk)
            if type_ == b'IDAT':
                if oper_type == 'ecb':
                    self.encrypt_data = rsa.ecb_encrypt(data)
                    chunk = specific_chunk(length, self.encrypt_data, type_, crc)
                else:
                    self.encrypt_data = rsa.cbc_encrypt(data)
                    chunk = specific_chunk(length, self.encrypt_data, type_, crc)
            else:
                chunk = specific_chunk(length, data, type_, crc)
            self.chunks.append(chunk)
            if type_ == b'IEND':
                self.file.seek(8)
                break

    def decrypt_chunks(self, oper_type):
        self.chunks = []
        keys = Keys(512)
        public_key = keys.generate_public_key()
        private_key = keys.generate_private_key()
        rsa = RSA(public_key, private_key)
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            data = self.file.read(int.from_bytes(length, 'big'))
            crc = self.file.read(Chunk.CRC_FIELD_LEN)
            specific_chunk = CHUNKTYPES.get(type_, Chunk)
            if type_ == b'IDAT':
                if oper_type == 'ecb':
                    self.encrypt_data = rsa.ecb_encrypt(data)
                    self.decrypt_data = rsa.ecb_decrypt(self.encrypt_data)
                    chunk = specific_chunk(length, self.decrypt_data, type_, crc)
                else:
                    self.encrypt_data = rsa.cbc_encrypt(data)
                    self.decrypt_data = rsa.cbc_decrypt(self.encrypt_data, self.after_iend_data)
                    chunk = specific_chunk(length, self.encrypt_data, type_, crc)
            else:
                chunk = specific_chunk(length, data, type_, crc)
            self.chunks.append(chunk)
            if type_ == b'IEND':
                self.file.seek(8)
                break

    def encrypt_from_lib(self):
        self.chunks = []
        keys = Keys(512)
        public_key = keys.generate_public_key()
        private_key = keys.generate_private_key()
        rsa = RSA(public_key, private_key)
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            data = self.file.read(int.from_bytes(length, 'big'))
            crc = self.file.read(Chunk.CRC_FIELD_LEN)
            specific_chunk = CHUNKTYPES.get(type_, Chunk)
            if type_ == b'IDAT':
                self.encrypt_data_from_library = rsa.crypto_library_encrypt(
                    data)
                chunk = specific_chunk(length, self.encrypt_data_from_library, type_, crc)
            else:
                chunk = specific_chunk(length, data, type_, crc)
            self.chunks.append(chunk)
            if type_ == b'IEND':
                self.file.seek(8)
                break

    def create_file(self, file_path, type_):
        new_file = open(file_path, 'wb')
        new_file.write(self.PNG_MAGIC_NUMBER)

        for chunk in self.chunks:
            if chunk.type_ in CRITICAL_CHUNKS_TABLE:
                new_file.write(chunk.length)
                new_file.write(chunk.type_)
                if chunk.type_ == b'IDAT':
                    if type_ == 'encrypt':
                        new_file.write(chunk.data)
                    if type_ == 'encrypt_lib':
                        new_file.write(self.encrypt_data_from_library)
                    else:
                        new_file.write(self.decrypt_data)
                else:
                    new_file.write(chunk.data)
                new_file.write(chunk.crc)

        new_file.close()

    def save_file(self, file_path):
        new_file = open(file_path, 'wb')
        new_file.write(self.PNG_MAGIC_NUMBER)
        for chunk in self.chunks:
            if chunk.type_ == b'IDAT':
                idat_data = bytes(self.encrypt_data)
                new_data, new_crc = self.compress_IDAT(idat_data)
                chunk_len = len(new_data)
                new_file.write(struct.pack('>I', chunk_len))
                new_file.write(chunk.type_)
                new_file.write(new_data)
                new_file.write(struct.pack('>I', new_crc))
            else:
                chunk_len = len(chunk.data)
                new_file.write(struct.pack('>I', chunk_len))
                new_file.write(chunk.type_)
                new_file.write(chunk.data)
                new_file.write(struct.pack('>I', int.from_bytes(chunk.crc, 'big')))
        new_file.close()
        return new_file

    def compress_IDAT(self, all_data):
        new_data = zlib.compress(all_data, 9)
        crc = zlib.crc32(new_data, zlib.crc32(struct.pack('>4s', b'IDAT')))
        return new_data, crc
