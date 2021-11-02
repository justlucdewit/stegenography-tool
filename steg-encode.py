import sys
from PIL import Image

# Stegenography encoding tool
# able to hide files in images
# will in the future also suport hiding other things like web URI's, entire
# folder structures, and executables
#
# Disclaimer: i am no expert on stegenography, i basically have no idea what the
# fuck i am doing, yet this seems to work so.... ¯\_(ツ)_/¯
#
# Coded by Luke_



# ------------------------------------------------------------------------------
# Some boring shit to setup for the rest of the program
# + Setup edge cases with argv inputs
# + Setup 'gathering buffer' to store the new generated pixels
# + Setup counting variable so we know which pixel to manipulate next
# ------------------------------------------------------------------------------
if len(sys.argv) <= 2:
	print("usage: python3 steg-encode.py hidden_file.extension image_to_hide_in.png")
	exit(1)

new_pixels = []
new_pixels_i = 0



# ------------------------------------------------------------------------------
# This will encode the file name into the first rgba values of the image
# 
# the r-values of these rgba chunks will all start with an even number to
# indicate that we are still in the file name chunk
# 
# The g-values will then encode a 1 or a 2, if the g-value is even thats a 1, if
# the g-value is odd, then thats a 0
# ------------------------------------------------------------------------------

_, message_file, container_file = sys.argv[0:]
input_image = Image.open(container_file)
pixels = list(input_image.getdata())
file_name_bits = ''.join(list(map(lambda x: format(ord(x), '08b'), message_file)))

for bit in file_name_bits:
	pixel = pixels[new_pixels_i]
	new_pixels_i += 1
	new_pixel_r = pixel[0]
	new_pixel_g = pixel[1]
	new_pixel_b = pixel[2]
	new_pixel_a = pixel[3]
	
	if new_pixel_r % 2 != 0:
		new_pixel_r = (new_pixel_r + 1) % 256

	if bit == '1':
		if new_pixel_g % 2 != 0:
			new_pixel_g = (new_pixel_g + 1) % 256

	elif bit == '0':
		if new_pixel_g % 2 == 0:
			new_pixel_g = (new_pixel_g + 1) % 256

	if new_pixel_b % 2 != 0:
		new_pixel_b = (new_pixel_b + 1) % 256
	
	new_pixels.append((new_pixel_r, new_pixel_g, new_pixel_b, new_pixel_a))



# ------------------------------------------------------------------------------
# This will encode the file content into the the rest of the rgba values of the
# image
# 
# the r-values of these rgba chunks will all start with an odd number to
# indicate that we are still in the file content section
# 
# The g-values will then encode a 1 or a 2, if the g-value is even thats a 1, if
# the g-value is odd, then thats a 0
# 
# Also make sure the b-value is even to indicate that these pixels are still
# part of the encoding
# ------------------------------------------------------------------------------

message_file_content = open(message_file).read()
file_content_bits = ''.join(list(map(lambda x: format(ord(x), '08b'), message_file_content)))

for bit in file_content_bits:
	pixel = pixels[new_pixels_i]
	new_pixels_i += 1
	new_pixel_r = pixel[0]
	new_pixel_g = pixel[1]
	new_pixel_b = pixel[2]
	new_pixel_a = pixel[3]
	
	if new_pixel_r % 2 == 0:
		new_pixel_r = (new_pixel_r + 1) % 256

	if bit == '1':
		if new_pixel_g % 2 != 0:
			new_pixel_g = (new_pixel_g + 1) % 256

	elif bit == '0':
		if new_pixel_g % 2 == 0:
			new_pixel_g = (new_pixel_g + 1) % 256
	
	if new_pixel_b % 2 != 0:
		new_pixel_b = (new_pixel_b + 1) % 256
	
	new_pixels.append((new_pixel_r, new_pixel_g, new_pixel_b, new_pixel_a))



# ------------------------------------------------------------------------------
# Now we will also copy the rest of the values over to finish the image
# The b-value will be set to uneven values to indicate that these values are no
# longer part of the encoding
# ------------------------------------------------------------------------------

for i in range(len(pixels) - len(new_pixels)):
	pixel = pixels[new_pixels_i]
	new_pixels_i += 1
	new_pixel_r = pixel[0]
	new_pixel_g = pixel[1]
	new_pixel_b = pixel[2]
	new_pixel_a = pixel[3]

	if new_pixel_b % 2 == 0:
		new_pixel_b = (new_pixel_b + 1) % 256

	new_pixels.append((new_pixel_r, new_pixel_g, new_pixel_b, new_pixel_a))



# ------------------------------------------------------------------------------
# Now that we have the encoded image data, we can save it
# ------------------------------------------------------------------------------

output_image = Image.new('RGBA', size=input_image.size)
output_image.putdata(new_pixels)
output_image.save(container_file.split('.')[0] + '-output.png')