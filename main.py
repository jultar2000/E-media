from PNG import *

png = PNG("images/China.png")
# png_service = PNGService(PNG("images/wolf"))
png.read_all_chunks()
png.print_chunks()

# print()
# print()
# print()
# print()
# png.create_file_only_with_critical_chunks("images/dupa.png")
# png2 = PNG("images/dupa.png")
# png2.read_all_chunks()
# png2.print_chunks()

# png.print_chunks()
# png.clear_chunks()
# png.read_critical_chunks()
# png.print_chunks()

