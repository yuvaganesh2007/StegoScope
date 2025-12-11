#!/usr/bin/env python3

from PIL import Image
import numpy as np
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("image", help="path to image")
args=parser.parse_args()

img=Image.open(args.image)
pixel_arr=np.asarray(img)
print(pixel_arr.shape)

for i in range(0,3):
    print(pixel_arr[0,i])
