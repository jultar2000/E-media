from PNG import *

path = "images/kolka.png"
new_image_path = "images/new_image2.png"

# types: encrypt, encrypt_Lib

png = PNG(path)
png.encrypt_data_from_library()
# png.create_file(new_image_path, "encrypt")
png.save_file(new_image_path)
