import PrimeNumGenerator

from PNG import *
from PrimeNumGenerator import *

# bang:
# IHDR, PLTE, IDAT, IEND

# switzerland
# IDHR, pHYs, cHRM, IDAT, IEND

# rocket
# IHDR, gAMA, cHRM, bKGD, IDAT, IEND

# kolka
# IHDR, tIME, IDAT, IEND

# pikaczu
# IHDR, gAMA, sRGB, cHRM, bKGD, IDAT, IEND

# path = "images/bang.png"
# new_image_path = "images/new_image.png"
#
# png = PNG(path)
# png.read_all_chunks()
# png.print_chunks()
# png.display_original_and_cleaned_file(path, 'new_image')
#
# print('----------------------------------------------')
#
# new_png = PNG(new_image_path)
# new_png.read_all_chunks()
# new_png.print_chunks()
# png.fourier_transform(path)
# new_png.fourier_transform(new_image_path)

num = PrimeNumGenerator.generate_prime_number()
print(num)
