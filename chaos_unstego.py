from PIL import Image
import random as rand
from math import log10, floor
import sys

# This program does the exact thing as chaos_stego.py, but in reverse

def nextCoord(R, X):
	return (R * X * (1 - X))

def round_sig(x, sig=6):
	return round(x, sig-int(floor(log10(abs(x))))-1)

pic = input("What is the path to the stego picture?\n > ").split(".")

im = Image.open(".".join(pic), formats=[pic[1]])

rateX, rateY, rateRGB = 0,0,0
x, y, rp = 0,0,0
length = 0

with open("key.txt", 'r') as keyfile:
	try:
		rateX = float(keyfile.readline()[:-2])
		x = float(keyfile.readline()[:-2])
		rateY = float(keyfile.readline()[:-2])
		y = float(keyfile.readline()[:-2])
		rateRGB = float(keyfile.readline()[:-2])
		rp = float(keyfile.readline()[:-2])
		length = int(keyfile.readline())
	except:
		sys.exit("There was a problem reading the key file")

pixel_map = im.load()
WIDTH, HEIGHT = im.size

decipher = ""

# DEBUG VARS HERE
rgbACT = ""

for z in range(length):

	xpix = floor(round_sig(x) * WIDTH)
	ypix = floor(round_sig(y) * HEIGHT)

	r, g, b = im.getpixel((xpix, ypix))

	bit = floor(round_sig(rp) * 3)

	if bit == 0:
		decipher += str(r % 2)
		rgbACT += "Red: {}\n".format(r)
	elif bit == 1:
		decipher += str(g % 2)
		rgbACT += "Green: {}\n".format(g)
	else:
		decipher += str(b % 2)
		rgbACT += "Blue: {}\n".format(b)

	x = nextCoord(round_sig(rateX), round_sig(x))
	y = nextCoord(round_sig(rateY), round_sig(y))
	rp = nextCoord(round_sig(rateRGB), round_sig(rp))


with open("debug_us.txt", 'w') as dbgfile:
	dbgfile.write(rgbACT)

bitlen = len(decipher)/8 

for i in range(int(bitlen)):
	start = i*8
	end = (i+1)*8
	print(chr(int(str(decipher[start:end]),2)), end="")