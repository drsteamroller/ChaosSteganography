from PIL import Image
import random as rand
from math import log10, floor

# Short for startPoint. It gives us the starting rate and X0/Y0.
# The function used is as follows: X_[n] = R * X_[n-1] * (1 - X_[n-1])
def startP():
	R = (400 - (rand.random() * 42))/100
	X0 = rand.random()

	return (R, X0)

# Here is the function for the next coordinate
def nextCoord(R, X):
	return (R * X * (1 - X))

# Helper function to pick between 0 - red, 1 - green, or 2 - blue
def pickRGB():
	return floor(rand.random() * 3)

# Short for determine bit insert. If the LSB and the input bit are the same,
# do nothing (return 0) otherwise, subtract 1 if our bit is 0 and add one if it's 1
def detBitInsert(bit, rgbval):
	if rgbval % 2 == int(bit):
		return 0

	else:
		if bit == "0":
			return -1
		else:
			return 1

# I'm not exactly sure if this helps, but this makes sure we use exactly 3
# significant features since float values in code are not exact.
def round_sig(x, sig=3):
	return round(x, sig-int(floor(log10(abs(x))))-1)

# This is highly assumptive that the user input is of the format
# "{name}.{picture extension}", but it reads in the picture from the same
# path as the program and then opens it with Pillow.
pic = input("What is the path to the cover picture?\n > ").split(".")
stegoImage = [pic[0]+"_altered", pic[1]]
im = Image.open(".".join(pic), formats=[pic[1]])

# Next, ask for the text file that will be implanted into the cover photo
textf = input("What is the path to the file to be implanted?\n > ")
filecontents = ""
with open(textf, 'r') as cipher:
	filecontents = cipher.read()

# Then convert it into binary
inbinary = ""
for x in filecontents:
	inbinary += str(format(ord(x), '08b'))

# Pick a starting point for the rates and x & y coordinates
sX = startP()
rateX, x = sX[0], sX[1]

sY = startP()
rateY, y = sY[0], sY[1]

# Open or create a key file that contains the starting values
with open("key.txt", 'w') as keyfile:
	keyfile.writelines([str(rateX), "\n", str(x), "\n", str(rateY), "\n", str(y), "\n"])

# Load the pixel map of rgb values and store the width and height of the image
pixel_map = im.load()
WIDTH, HEIGHT = im.size

# stores 0, 1, 2 for r, g, b respectively for each bit inserted
rgbStream = []

# Error checking list that grabs all the coordinates so I can compare
# it to when the reverse process runs (purely for debugging)
coords = []

# For each bit in the supplied message, find a coordinate in the image,
# then determine if we need to change the LSB, and then change it in the
# pixel_map. Then find the next coordinate and repeat.
for bit in inbinary:

	xpix = floor(round_sig(x) * WIDTH)
	ypix = floor(round_sig(y) * HEIGHT)

	coords.append((xpix,ypix))

	r, g, b, p = im.getpixel((xpix, ypix))
	
	rgb = pickRGB()
	rgbStream.append(rgb)

	if rgb == 0:
		val = detBitInsert(bit, r)
		r = r+val
	elif rgb == 1:
		val = detBitInsert(bit, g)
		g = g+val
	else:
		val = detBitInsert(bit, b)
		b = b+val

	pixel_map[xpix,ypix] = (r, g, b)
	x = nextCoord(round_sig(rateX), round_sig(x))
	y = nextCoord(round_sig(rateY), round_sig(y))

# Append the rgbStream into the key file (will replace with its own
# chaos function implementation to cut down key file size)
with open("key.txt", 'a') as keyfile:
	keyfile.write(str(rgbStream))

# More debugging
with open("stego_coords.txt", 'w') as coordfile:
	for i in coords:
		coordfile.write(str(i) + "\n")

# Save the stego-image
im.save(".".join(stegoImage), formats=[pic[1]])