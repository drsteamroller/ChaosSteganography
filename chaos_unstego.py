from PIL import Image
import random as rand
from math import log10, floor
import sys

# This program does the exact thing as chaos_stego.py, but in reverse

def nextCoord(R, X):
	return (R * X * (1 - X))

def round_sig(x, sig=3):
	return round(x, sig-int(floor(log10(abs(x))))-1)

pic = input("What is the path to the stego picture?\n > ").split(".")

im = Image.open(".".join(pic), formats=[pic[1]])

keycontents = []

with open("key.txt", 'r') as keyfile:
	rateX, x, rateY, y, rgbStream = 0,0,0,0,[]
	try:
		rateX = float(keyfile.readline()[:-2])
		x = float(keyfile.readline()[:-2])
		rateY = float(keyfile.readline()[:-2])
		y = float(keyfile.readline()[:-2])
		res = keyfile.readline()
		rgbStream = res[1:-1].split(', ')
	except:
		sys.exit("There was a problem reading the key file")

	for h in range(len(rgbStream)):
		rgbStream[h] = int(rgbStream[h])

	keycontents = [rateX, x, rateY, y, rgbStream]

pixel_map = im.load()
WIDTH, HEIGHT = im.size
x, y = keycontents[1], keycontents[3]

decipher = ""

coords = []

for bit in keycontents[4]:

	xpix = floor(round_sig(x) * WIDTH)
	ypix = floor(round_sig(y) * HEIGHT)

	coords.append((xpix, ypix))

	r, g, b = im.getpixel((xpix, ypix))

	if bit == 0:
		decipher += str(r % 2)
	elif bit == 1:
		decipher += str(g % 2)
	else:
		decipher += str(b % 2)

	x = nextCoord(round_sig(rateX), round_sig(x))
	y = nextCoord(round_sig(rateY), round_sig(y))


with open("unstego_coords.txt", 'w') as coordfile:
	for i in coords:
		coordfile.write(str(i) + "\n")

bitlen = len(decipher)/8 

for i in range(int(bitlen)):
	start = i*8
	end = (i+1)*8
  print (chr(int(str(decipher[start:end]),2)), end="")
print()