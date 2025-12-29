import numpy as np
from PIL import Image

def LSBHistogram(input_image):
    count1=0
    count0=0
    print("LSB Histogram text is selected")
    img=Image.open(input_image).convert("RGB")
    pixel_array=np.asarray(img)
    pixel_arr=pixel_array.flatten()
    print(len(pixel_arr))
    for i in pixel_arr:
        if i%2==0:
            count0+=1
        else:
            count1+=1
    print(abs(count1-count0)/(count0+count1))
def ChiSquare(input_image):
    print("Chi Square test is selected")
    img=Image.open(input_image).convert("RGB")
    pixel_array=np.asarray(img)
