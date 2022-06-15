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
        self.after_iend_data = bytearray()
        self.decrypt_data = bytearray()
        self.encrypt_data_from_library = bytearray()
        self.after_iend_data__from_library = bytearray()

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

    def read_all_chunks_for_rsa_ecb(self):
        self.chunks = []
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            data = self.file.read(int.from_bytes(length, 'big'))
            crc = self.file.read(Chunk.CRC_FIELD_LEN)
            specific_chunk = CHUNKTYPES.get(type_, Chunk)
            chunk = specific_chunk(length, data, type_, crc)
            if type_ == b'IDAT':
                keys = Keys(512)
                public_key = keys.generate_public_key()
                private_key = keys.generate_private_key()
                rsa = RSA(public_key, private_key)
                self.encrypt_data, self.after_iend_data = rsa.ecb_encrypt(data)
                self.decrypt_data = rsa.ecb_decrypt(self.encrypt_data, self.after_iend_data)
                self.encrypt_data_from_library, self.after_iend_data__from_library = rsa.crypto_library_encrypt(
                    data)
            self.chunks.append(chunk)
            if type_ == b'IEND':
                self.file.seek(8)
                break

    # def IDAT_chunk_processor_cbc(self):
    #     IDAT_data = b''.join(chunk.chunk_data for chunk in self.chunks
    #                          if chunk.chunk_type == b'IDAT')
    #     IDAT_data = zlib.decompress(IDAT_data)
    #     IDAT_filter = IDATFilter(self.width, self.height, IDAT_data)
    #     information = IDAT_filter.print_recon_pixels()
    #     print(information)
    #     keys = Keys(512)
    #     public_key = keys.generate_public_key()
    #     private_key = keys.generate_private_key()
    #     rsa = RSA(public_key, private_key)
    #     self.encrypt_data, self.after_iend_data = rsa.cbc_encrypt(IDAT_data)
    #     self.decrypt_data = rsa.cbc_decrypt(self.encrypt_data, self.after_iend_data)

    def read_all_chunks_for_rsa_cbc(self):
        self.chunks = []
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            data = self.file.read(int.from_bytes(length, 'big'))
            crc = self.file.read(Chunk.CRC_FIELD_LEN)
            if type_ == b'IDAT':
                print('dupa')
                # tutaj wstawiamy konwerter
            else:
                specific_chunk = CHUNKTYPES.get(type_, Chunk)
                chunk = specific_chunk(length, data, type_, crc)
            self.chunks.append(chunk)
            if type_ == b'IEND':
                self.file.seek(8)
                break

    def read_critical_chunks(self):
        self.chunks = []
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            data = self.file.read(int.from_bytes(length, 'big'))
            crc = self.file.read(Chunk.CRC_FIELD_LEN)
            if type_ in CRITICAL_CHUNKS_TABLE:
                specific_chunk = CHUNKTYPES.get(type_, Chunk)
                chunk = specific_chunk(length, data, type_, crc)
                self.chunks.append(chunk)
            if type_ == b'IEND':
                self.file.seek(8)
                break

    def create_file_only_with_critical_chunks(self, file_path):
        new_file = open(file_path, 'wb')
        new_file.write(self.PNG_MAGIC_NUMBER)

        for chunk in self.chunks:
            if chunk.type_ in CRITICAL_CHUNKS_TABLE:
                new_file.write(chunk.length)
                new_file.write(chunk.type_)
                new_file.write(chunk.data)
                new_file.write(chunk.crc)

        new_file.close()

    def create_ecb_file(self, file_path):
        new_file = open(file_path, 'wb')
        new_file.write(self.PNG_MAGIC_NUMBER)

        for chunk in self.chunks:
            if chunk.type_ in CRITICAL_CHUNKS_TABLE:
                new_file.write(chunk.length)
                new_file.write(chunk.type_)
                if chunk.type_ == b'IDAT':
                    new_file.write(self.encrypt_data)
                else:
                    new_file.write(chunk.data)
                new_file.write(chunk.crc)

        new_file.close()
