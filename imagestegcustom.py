import numpy as np
from PIL import Image
import argparse as ap
import sys

parser=ap.ArgumentParser()
parser.add_argument("file", help="image file to handle")
parser.add_argument("--extract","-e", action="store_true", help="choose to extract")
parser.add_argument("--embed", "-E", action="store_true", help="to embed data into the file")
args=parser.parse_args()

path=str(args.file)
img=Image.open(args.file)
pixel_array=np.asarray(img)
new_pixel_array=pixel_array.copy()
shape=pixel_array.shape
if(args.extract):
    print("Extraction of hidden data is selected(custom method)")
    print("Processing...")
   # shape=pixel_array.shape
    i=0
    j=0
    data=""
    while True:
        trash_arr=np.append(pixel_array[j,i],pixel_array[j,i+1], axis=0)
        pixarr=np.append(trash_arr, pixel_array[j,i+2], axis=0)
        if i>=shape[1]:
            j+=1
            i=0
        i+=3
        bin_arr=['0','0','0','0','0','0','0','0']
        for k in range(1,9):
            if pixarr[k]%2==0:
                bin_arr[k-1]='1'
            else:
                bin_arr[k-1]='0'
        fin_bin_arr="".join(bin_arr)
        int_bin=int(fin_bin_arr, 2)
        char=chr(int_bin)
        data=data+char
        if (pixarr[0]%2==1):
            break
    print(f"The extracted hidden data is: {data}")

elif(args.embed):
    print("Embedding data into image is selected(custom method)...")
    data=input("Enter the data to embed into the image file: ")
    #shape=pixel_array.shape
    i=0
    j=0
    for char in data:
        if i>=shape[1]:
            j+=1
            i=0
        trash_arr=np.append(pixel_array[j,i],pixel_array[j,i+1], axis=0)
        pixarr=np.append(trash_arr, pixel_array[j,i+2], axis=0)
        #i+=3
        ascii_val=ord(char)
        binary=format(ascii_val,' 08b')
        bin_str="0"+str(binary)[1:]
        k=1
        for digit in bin_str:
            if digit=='0':
                if (pixarr[k]%2==0):
                    if pixarr[k]==0:
                        pixarr[k]+=1
                    else:
                        pixarr[k]-=1
            else:
                if (pixarr[k]%2!=0):
                    pixarr[k]-=1
            k+=1
            if(pixarr[0]%2==1):
                pixarr[0]-=1
        new_pixel_array[j,i]=pixarr[0:3]
        new_pixel_array[j,i+1]=pixarr[3:6]
        new_pixel_array[j,i+2]=pixarr[6:9]
        i+=3
    if new_pixel_array[j,i-3,0]%2==0:
        if(new_pixel_array[j,i-3,0]==0):
            new_pixel_array[j,i-3,0]+=1
        else:
            new_pixel_array[j,i-3,0]-=1
    output_image=Image.fromarray(new_pixel_array)
    print("Data embedded successfully into the image")
    print("Choices:\n 1. Show output image\n 2. Save output image\n")
    choice=int(input("Enter your choice: "))
    if choice==1:
        print("processing...")
        output_image.show()
    elif choice==2:
        new_name=input("Enter the name of the new image file(.png): ")
        print("Saving...")
        new_path=f"/home/yuvaganesh/Pictures/embedded_images/"+new_name
        output_image.save(new_path)
    else:
        print("Invalid choice")

