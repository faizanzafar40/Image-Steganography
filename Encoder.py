from PIL import Image, ImageFilter
import binascii
import random

from HelperFunctions import *

def myEncoder(fileName,number):
    with open(fileName, "r") as myfile:
        data = myfile.read()

    testBin = return_binary(data) + '10000000000000000000000000000000000000000'
    binLength = len(testBin)

    # open image
    image = Image.open(str(random.randrange(1, 6)) + '.png')

    # store size
    length,height = image.size

    # split into three bands
    imageLoaded = image.load()

    # start encoding from the first bit
    index = 0

    # loop over all pixel values
    for x in range(0,height-1):
        for y in range(0,length-1):

            r,g,b = imageLoaded[y,x]
            # encoding in RED
            if index < binLength:
                if testBin[index] == '0':
                    r = clear_last_bit(r)
                else:
                    r = set_last_bit(r)
                index = index + 1
            else:
                break

            # encoding in GREEN
            if index < binLength:
                if testBin[index] == '0':
                    g = clear_last_bit(g)
                else:
                    g = set_last_bit(g)
                index = index + 1
            else:
                break

            # encoding in BLUE
            if index < binLength:
                if testBin[index] == '0':
                    b = clear_last_bit(b)
                else:
                    b = set_last_bit(b)
                index = index + 1
            else:
                break

            imageLoaded[y,x] = (r, g, b)

    # Saving the image
    image.save(number + 'modified.png', 'PNG')
