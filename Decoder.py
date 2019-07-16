from PIL import Image, ImageFilter
import binascii

from HelperFunctions import *

# SET IMAGE FILENAME HERE WHICH YOU WANT TO DECODE

imageName = '1modified.png'

# open image
image = Image.open(imageName)

# store size
length,height = image.size

# split into three bands
imageLoaded = image.load()

index = 0
counter = 0

decodedBin = ''

# loop over all pixel values
for x in range(0,height-1):
  for y in range(0,length-1):

    # decode one bit from every byte of data
    # stop when terminating 0000s are found
    r,g,b = imageLoaded[y,x]

    if counter != 35:
      bit = r & 1
      decodedBin = decodedBin + str(bit)
      if bit == 0:
        counter = counter + 1
      else:
        counter = 0
    else:
      break

    if counter != 35:
      bit = g & 1
      decodedBin = decodedBin + str(bit)
      if bit == 0:
        counter = counter + 1
      else:
        counter = 0
    else:
      break

    if counter != 35:
      bit = b & 1
      decodedBin = decodedBin + str(bit)
      if bit == 0:
        counter = counter + 1
      else:
        counter = 0
    else:
      break

decodedBin = decodedBin[0:len(decodedBin)-counter-1] # remove the terminating bits we put earlier while encoding data

print(return_text(decodedBin))

