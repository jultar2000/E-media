from PNG import *

png = PNG("images/lena.png")
# png_service = PNGService(PNG("images/wolf"))
png.read_all_chunks()
png.print_chunks()
# png.fourier_transform("images/lena.png")

