from PNG import *

path = "images/wolf.png"
new_image_path = "images/new_image.png"

png = PNG(path)
png.read_all_chunks()
png.print_chunks()

png.display_original_and_cleaned_file(path, 'new_image')

print('----------------------------------------------')

new_png = PNG(new_image_path)
new_png.read_all_chunks()
new_png.print_chunks()

png.fourier_transform(path)
new_png.fourier_transform(new_image_path)
