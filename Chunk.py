class Chunk:
    LENGTH_FIELD_LEN = 4
    TYPE_FIELD_LEN = 4
    CRC_FIELD_LEN = 4

    def __init__(self, length, type_, crc):
        self.length = length
        self.type_ = type_
        self.crc = crc


CHUNK_TYPES = {
    b'IHDR': IHDR,
    b'IDAT': IDAT,
    b'IEND': IEND,
}
