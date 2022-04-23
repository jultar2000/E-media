import codecs
import struct


class Chunk:
    LENGTH_FIELD_LEN = 4
    TYPE_FIELD_LEN = 4
    CRC_FIELD_LEN = 4

    def __init__(self, length, data, type_, crc):
        self.length = length
        self.data = data
        self.type_ = type_
        self.crc = crc

    def __str__(self):
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    Length: " + str(int.from_bytes(self.length, 'big')))
        # print("    Data: " + str(self.data))
        print("    CRC: " + self.crc.hex())


class IHDR(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

        values = struct.unpack('>iibbbbb', self.data)
        self.width = str(values[0])
        self.height = str(values[1])
        self.bit_depth = str(values[2])
        self.color_type = str(values[3])
        self.compression_method = str(values[4])
        self.filter_method = str(values[5])
        self.interlace_method = str(values[6])

    def __str__(self):
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    Width: " + self.width)
        print("    Height: " + self.height)
        print("    Bit_depth: " + self.bit_depth)
        print("    Color_type: " + self.color_type)
        print("    Compression_method: " + self.compression_method)
        print("    Filter_method: " + self.filter_method)
        print("    Interlace_method: " + self.interlace_method)


class IDAT(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)


class IEND(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

    def __str__(self):
        return super().__str__()


CHUNKTYPES = {
    b'IHDR': IHDR,
    # b'PLTE': PLTE,
    b'IDAT': IDAT,
    b'IEND': IEND
    # b'tIME': tIME,
    # b'gAMA': gAMA,
    # b'cHRM': cHRM,
}

critical_chunks_table = [b'IHDR', b'IDAT', b'IEND']
