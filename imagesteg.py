import numpy as np
from PIL import Image
import argparse
import sys
from steganalysis.imageanalysis import LSBHistogram, ChiSquare

parser=argparse.ArgumentParser()
parser.add_argument("file", help="image file to handle")
parser.add_argument("--extract","-e", action="store_true", help="choose to extract")
parser.add_argument("--embed", "-E", action="store_true", help="to embed data into the file")
parser.add_argument("--analyze", "-a", action="store_true", help="to analyze the file")
group=parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args=parser.parse_args()

path=str(args.file)
img=Image.open(args.file).convert("RGB")
pixel_array=np.asarray(img)
new_pixel_array=pixel_array.copy()
shape=pixel_array.shape

if(args.extract):
    if args.verbose:
        print("Extraction of hidden data is selected")
        print("Processing...")
    i=0
    j=0
    data=""
    while True:
        if i>=shape[1]-2:
            j+=1
            i=0
        trash_arr=np.append(pixel_array[j,i],pixel_array[j,i+1], axis=0)
        pixarr=np.append(trash_arr, pixel_array[j,i+2], axis=0)
        i+=3
        bin_arr=['0','0','0','0','0','0','0','0']
        for k in range(0,8):
            if pixarr[k]%2==0:
                bin_arr[k]='0'
            else:
                bin_arr[k]='1'
        fin_bin_arr="".join(bin_arr)
        int_bin=int(fin_bin_arr, 2)
        char=chr(int_bin)
        data=data+char
        if (pixarr[-1]%2==1):
            break
    print("Choices for outputting data:\n1. Output to stdout\n2. Output to a file")
    output_type=int(input("Enter the type of output for data: "))
    if output_type==1:
        print(f"The extracted hidden data is:\n {data}")
    elif output_type==2:
        output_path=input("Enter the path of the output data file:")
        with open(output_path, "w") as file:
            file.write(data)
        print("Hidden data is successfully written into the output file")
    else:
        print("Invalid choice is selected")
        if args.verbose:
            print("Aborting...")
        sys.exit(1)

elif(args.embed):
    if args.verbose:
        print("Embedding data into image is selected...")
    print("Choices for inputting data:\n1. Input from keyboard(type the data)\n2. Input from a file")
    input_type=int(input("Enter the type of input of data: "))
    if input_type==1:
        data=input("Enter the data to embed into the image file: ")
    elif input_type==2:
        input_path=input("Enter the path of the input data file:")
        with open(input_path, "r") as file:
            data=file.read()
    else:
        print("Invalid choice is selected")
        if args.verbose:
            print("Aborting...")
        sys.exit(1)

    if((len(data)*8)>(shape[0]*shape[1]*shape[2])):
        print("The data is too long to embed into the image given")
        if args.verbose:
            print("Aborting...")
        sys.exit(1)
    i=0
    j=0
    for char in data:
        if i>=shape[1]-2:
            j+=1
            i=0
        trash_arr=np.append(pixel_array[j,i],pixel_array[j,i+1], axis=0)
        pixarr=np.append(trash_arr, pixel_array[j,i+2], axis=0)
        ascii_val=ord(char)
        binary=format(ascii_val,' 08b')
        bin_str="0"+str(binary)[1:]
        k=0
        for digit in bin_str:
            if digit=='0':
                if pixarr[k]%2==1:
                    pixarr[k]-=1
            else:
                if pixarr[k]%2==0:
                    pixarr[k]+=1
            k+=1
            if(pixarr[-1]%2==1):
                pixarr[-1]-=1
        new_pixel_array[j,i]=pixarr[0:3]
        new_pixel_array[j,i+1]=pixarr[3:6]
        new_pixel_array[j,i+2]=pixarr[6:9]
        i+=3
    if new_pixel_array[j,i-1,-1]%2==0:
        new_pixel_array[j,i-1,-1]+=1

    output_image=Image.fromarray(new_pixel_array)
    if args.verbose:
        print("Data embedded successfully into the image")
    print("Choices:\n 1. Show output image\n 2. Save output image\n")
    choice=int(input("Enter your choice: "))
    if choice==1:
        if args.verbose:
            print("Processing...")
        output_image.show()
    elif choice==2:
        new_name=input("Enter the name of the new image file(.png): ")
        if args.verbose:
            print("Saving...")
        new_path=f"/home/yuvaganesh/Pictures/embedded_images/"+new_name
        output_image.save(new_path)
    else:
        print("Invalid choice is selected")
        if args.verbose:
            print("Aborting...")
        sys.exit(1)
elif(args.analyze):
    print("analysis selected")
    LSBHistogram(args.file)
    ChiSquare(args.file)

        
