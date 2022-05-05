from PNG import *

path = "images/dice.png"

png = PNG(path)
# png_service = PNGService(PNG("images/wolf"))
png.read_all_chunks()
png.print_chunks()
# png.fourier_transform(path)
png.display_original_and_cleaned_file(path, 'new_image')

# png.fourier_transform("images/lena.png")

