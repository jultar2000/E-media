from matplotlib import image as mpimg, pyplot as plt
from Chunk import *


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
