import sys
from PIL import Image

# Stegenography decoding tool
# able to retrieve files from images
# will in the future also suport retrieving other things like web URI's, entire
# folder structures, and executables
#
# Disclaimer: i am no expert on stegenography, i basically have no idea what the
# fuck i am doing, yet this seems to work so.... ¯\_(ツ)_/¯
#
# Coded by Luke_

# ------------------------------------------------------------------------------
# Some boring shit to setup for the rest of the program
# + Setup edge cases with argv inputs
# ------------------------------------------------------------------------------

if len(sys.argv) <= 1:
	print("usage: python3 steg-decode.py image.png")
	exit(1)



# ------------------------------------------------------------------------------
# Open the file from the file name in the argv, and retrieve the data
# ------------------------------------------------------------------------------
file_name = sys.argv[1]
image_data = list(Image.open(file_name).getdata())
image_data = list(filter(lambda x: x[2] % 2 == 0, image_data))

# ------------------------------------------------------------------------------
# Now filter out the pixels whose r-value are even to retrieve the file name
# ------------------------------------------------------------------------------
file_name = ''.join(list(map(lambda x: chr(int(x, base=2)), map(''.join, zip(*[iter(''.join(map(lambda x: '1' if x[1] % 2 == 0 else '0', list(filter(lambda x: x[0] % 2 == 0, image_data)))))]*8)))))

# ------------------------------------------------------------------------------
# Now filter out the pixels whose r-value are odd to retrieve the file data
# ------------------------------------------------------------------------------
file_content = ''.join(list(map(lambda x: chr(int(x, base=2)), map(''.join, zip(*[iter(''.join(map(lambda x: '1' if x[1] % 2 == 0 else '0', list(filter(lambda x: x[0] % 2 != 0, image_data)))))]*8)))))

# ------------------------------------------------------------------------------
# Now create and write to this file
# ------------------------------------------------------------------------------
f = open(file_name, "w")
f.write(file_content)
f.close()