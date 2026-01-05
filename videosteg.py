import numpy as np
from PIL import Image
import argparse
import sys
import subprocess
import os
import re

parser=argparse.ArgumentParser()
parser.add_argument("file", help="image file to handle")
parser.add_argument("--extract","-e", action="store_true", help="choose to extract")
parser.add_argument("--embed", "-E", action="store_true", help="to embed data into the file")
parser.add_argument("--analyze", "-a", action="store_true", help="to analyze the file")
group=parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args=parser.parse_args()

def imgExtract(image):
    path=str(image)
    img=Image.open(image).convert("RGB")
    pixel_array=np.asarray(img)
    new_pixel_array=pixel_array.copy()
    shape=pixel_array.shape
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
        
    return data

def imgEmbed(image, data):
    path=str(image)
    img=Image.open(image).convert("RGB")
    pixel_array=np.asarray(img)
    new_pixel_array=pixel_array.copy()
    shape=pixel_array.shape
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
    
    return output_image

def extract_frames(video_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i", video_path,
        os.path.join(out_dir, "frame_%06d.png")
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

extract_frames(args.file, "/home/yuvaganesh/StegoScope/tmpdir")

os.system(f"ffmpeg -i {args.file} -vf showinfo -f null - 2>&1 | grep ':I' >> new.txt")
os.system("awk '{print $5}' new.txt >>num.txt")

kf_numbers=[]
with open ("/home/yuvaganesh/StegoScope/num.txt","r") as file:
    for line in file:
        l=line.strip()
        n=int(l)
        n+=1
        kf_numbers.append(n)
trashlist=[f"{n:06d}.png" for n in kf_numbers]
formatted_num=tuple(trashlist)
kf_files=[]
p="/home/yuvaganesh/StegoScope/tmpdir"
for roots,dirs,files in os.walk(p):
    for filename in files:
        if filename.endswith(formatted_num):
            kf_files.append(filename)
sorted_files = sorted(kf_files, key=lambda x: int(re.findall(r'\d+', x)[-1]))
count_kf=len(sorted_files)

if(args.extract):
    if args.verbose:
        print("Extraction of hidden data is selected")
        print("Processing...")
    data=''
    for i in range(0,count_kf):
        path=os.path.join(p,sorted_files[i])
        data+=imgExtract(path)

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
        print("Embedding data into video is selected...")
    print("Choices for inputting data:\n1. Input from keyboard(type the data)\n2. Input from a file")
    input_type=int(input("Enter the type of input of data: "))
    if input_type==1:
        data=input("Enter the data to embed into the video file: ")
    elif input_type==2:
        input_path=input("Enter the path of the input data file:")
        with open(input_path, "r") as file:
            data=file.read()
    else:
        print("Invalid choice is selected")
        if args.verbose:
            print("Aborting...")
        sys.exit(1)
    chunk_no=len(data)//(count_kf-1)
    last_chunk=0
    if((len(data))%(count_kf-1)!=0):
        last_chunk=(len(data))%(count_kf-1)
    data_chunks=[]
    for i in range(0,count_kf-1):
        data_chunks.append(data[i*chunk_no:(i+1)*chunk_no])
    data_chunks.append(data[-last_chunk:])
    
    for i in range(0,count_kf):
        path=os.path.join(p,sorted_files[i])
        new_image=imgEmbed(path,data_chunks[i])
        new_image.save(path)
    if args.verbose:
        print("Data embedded successfully into the video")
    output_file=str(input("Enter the name of the output file(.mp4)"))
    output_path="/home/yuvaganesh/Videos/embedded_videos/"+output_file
    cmd = [
    "ffmpeg",
    "-y",
    "-framerate", "30",
    "-i", f"{p}/frame_%06d.png",
    "-start_number", "1",
    "-c:v", "libx264",
    "-crf", "0",
    "-pix_fmt", "yuv444p",
    output_path
    ]

    subprocess.run(cmd)

elif(args.analyze):
    print("Analysis selected")

os.system("rm -r /home/yuvaganesh/StegoScope/tmpdir")
os.system("rm /home/yuvaganesh/StegoScope/num.txt")
os.system("rm /home/yuvaganesh/StegoScope/new.txt")
