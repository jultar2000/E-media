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

    def display_file(self):
        tmp_png = self.file
        tmp_png.seek(0)
        img = mpimg.imread(tmp_png)
        plt.imshow(img)
        plt.show()

    def read_chunks(self):
        while True:
            length = self.file.read(Chunk.LENGTH_FIELD_LEN)
            type_ = self.file.read(Chunk.TYPE_FIELD_LEN)
            crc = self.file.read(Chunk.CRC_FIELD_LEN)

    def create_file_without_ancillary_chunks(self, file_name):
        critical_chunks_table = [b'IHDR', b'IDAT', b'IEND']
        file = open(file_name, 'wb')
        file.write(self.PNG_MAGIC_NUMBER)
