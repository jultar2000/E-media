import codecs
import struct
import zlib

from matplotlib import pyplot as plt
import numpy as np


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

    def get_width_height(self):
        return self.width, self.height,

    def __str__(self):
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    Width: " + self.width)
        print("    Height: " + self.height)
        print("    Bit_depth: " + self.bit_depth)
        print("    Color_type: " + self.color_type)
        print("    Compression_method: " + self.compression_method)
        print("    Filter_method: " + self.filter_method)
        print("    Interlace_method: " + self.interlace_method)


class IDAT():
    def __init__(self, width, height, length, data, type_, crc):
        self.recon_pixels = []
        self.bytes_per_pixel = 4
        self.width = width
        self.length = length
        self.crc = crc
        self.type_ = type_
        self.data = data
        self.height = height
        self.stride = width * self.bytes_per_pixel

    @staticmethod
    def paeth_predictor(a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            Pr = a
        elif pb <= pc:
            Pr = b
        else:
            Pr = c
        return Pr

    def recon_a(self, r, c):
        if c >= self.bytes_per_pixel:
            return self.recon_pixels[r * self.stride + c -
                                     self.bytes_per_pixel]
        return 0

    def recon_b(self, r, c):
        if r > 0:
            return self.recon_pixels[(r - 1) * self.stride + c]
        return 0

    def recon_c(self, r, c):
        if r > 0 and c >= self.bytes_per_pixel:
            return self.recon_pixels[(r - 1) * self.stride + c -
                                     self.bytes_per_pixel]
        return 0

    def __str__(self):
        zobj = zlib.decompressobj()
        IDAT_data = zobj.decompress(self.data)
        i = 0
        for r in range(self.height):
            filter_type = IDAT_data[i]
            i += 1
            for c in range(self.stride):
                filt_x = IDAT_data[i]
                i += 1
                if filter_type == 0:
                    recon_x = filt_x
                elif filter_type == 1:
                    recon_x = filt_x + self.recon_a(r, c)
                elif filter_type == 2:
                    recon_x = filt_x + self.recon_b(r, c)
                elif filter_type == 3:
                    recon_x = filt_x + (self.recon_a(r, c)
                                        + self.recon_b(r, c)) // 2
                elif filter_type == 4:
                    recon_x = filt_x + self.paeth_predictor(self.recon_a(r, c),
                                                            self.recon_b(r, c), self.recon_c(r, c))
                else:
                    raise Exception('unknown filter type: ' + str(filter_type))
                self.recon_pixels.append(recon_x & 0xff)
        plt.imshow(np.array(self.recon_pixels).reshape((self.height, self.width, 4)))
        plt.title('Recon pixels plot')
        plt.show()


class IEND(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)


class gAMA(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

    def __str__(self):
        gamma = int.from_bytes(self.data, 'big') / 100000
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    Gamma number:" + str(gamma))


class sRGB(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

    def __str__(self):
        values = struct.unpack('>b', self.data)
        color = values[0]
        colors_dic = {
            0: "Perceptual",
            1: "Relative colorimetric",
            2: "Saturation",
            3: "Absolute colorimetric"
        }

        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    Color space: " + str(color))
        print("    Type: " + colors_dic.get(color))


class cHRM(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

    def __str__(self):
        values = struct.unpack('>iiiiiiii', self.data)
        WPx = values[0] / 100000
        WPy = values[1] / 100000
        Rx = values[2] / 100000
        Ry = values[3] / 100000
        Gx = values[4] / 100000
        Gy = values[5] / 100000
        Bx = values[6] / 100000
        By = values[7] / 100000
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    WhitePointX: " + str(WPx))
        print("    WhitePointY: " + str(WPy))
        print("    RedX: " + str(Rx))
        print("    RedY: " + str(Ry))
        print("    GreenX: " + str(Gx))
        print("    GreenY: " + str(Gy))
        print("    BlueX: " + str(Bx))
        print("    BlueY: " + str(By))


class tIME(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

    def __str__(self):
        values = struct.unpack('>hbbbbb', self.data)
        year = values[0]
        month = values[1]
        day = values[2]
        hour = values[3]
        minute = values[4]
        second = values[5]
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    Last modification: "
              + str(year) + '/' + str(month) + '/' + str(day)
              + ' ' + str(hour) + ':' + str(minute) + ':' + str(second))


class pHYs(Chunk):
    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

    def __str__(self):
        values = struct.unpack('>iib', self.data)
        pixX = values[0]
        pixY = values[1]
        unit = values[2]
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        print("    X-axis: " + str(pixX))
        print("    Y-axis: " + str(pixY))
        print("    unit: " + str(unit))


class PLTE(Chunk):
    palette = []

    def __init__(self, length, type_, data, crc):
        super().__init__(length, type_, data, crc)

    def parse_data(self):
        for i in range(0, len(self.data), 3):
            part_pix = self.data[i:i + 3]
            full_pixel = (part_pix[0], part_pix[1], part_pix[2])
            if not self.palette.__contains__(full_pixel):
                self.palette.append(full_pixel)

    def __str__(self):
        self.parse_data()
        print("Chunk: " + codecs.decode(self.type_, 'UTF-8'))
        for color in self.palette:
            print(colored(color[0], color[1], color[2], str(color)))


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


CHUNKTYPES = {
    b'IHDR': IHDR,
    b'PLTE': PLTE,
    b'IDAT': IDAT,
    b'IEND': IEND,
    b'sRGB': sRGB,
    b'tIME': tIME,
    b'gAMA': gAMA,
    b'pHYs': pHYs,
    b'cHRM': cHRM
}

CRITICAL_CHUNKS_TABLE = [b'IHDR', b'PLTE', b'IDAT', b'IEND']
