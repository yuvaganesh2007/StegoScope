import wave
import numpy as np
import argparse
import sys 

parser=argparse.ArgumentParser()

parser.add_argument("file", help="image file to handle")
parser.add_argument("--extract","-e", action="store_true", help="choose to extract hidden data")
parser.add_argument("--embed", "-E", action="store_true", help="to embed data into the file")
group=parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args=parser.parse_args()

audio=wave.open(args.file)
params=audio.getparams()
frames=audio.readframes(-1)
sample_width=audio.getsampwidth()
audio.close()

if sample_width==1:
    samples=np.frombuffer(frames, dtype=np.uint8)
elif sample_width==2:
    samples=np.frombuffer(frames, dtype=np.int16)
elif sample_width==4:
    samples=np.frombuffer(frames, dtype=np.int32)
else:
    print("Invalid sample width detected")
    if args.verbose:
        print("Aborting...")
    sys.exit(1)

EOF_marker="11111110"

if(args.extract):
    if args.verbose:
        print("Extraction of hidden data is selected")
        print("Processing...")
    bin_str=''
    k=0
    while True:
        if samples[k]%2==0:
            bin_str+='0'
        else:
            bin_str+='1'
        k+=1
        if bin_str.endswith(EOF_marker):
            break

    bin_fin=bin_str[:-(len(EOF_marker))]
    i=0
    bin_list=[]
    while i<len(bin_fin):
        bin_list.append(bin_fin[i:8+i])
        i+=8
    char_list=[]
    for string in bin_list:
        int_str=int(string, 2)
        char_list.append(chr(int_str))
    data=''.join(char_list)
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
        print("Embedding data into audio file is selected...")
    print("Choices for inputting data:\n1. Input from keyboard(type the data)\n2. Input from a file")
    input_type=int(input("Enter the type of input of data: "))
    if input_type==1:
        data=input("Enter the data to embed into the audio file: ")
    elif input_type==2:
        input_path=input("Enter the path of the input data file:")
        with open(input_path, "r") as file:
            data=file.read()
    else:
        print("Invalid choice is selected")
        if args.verbose:
            print("Aborting...")
        sys.exit(1)
    bin_list=[]
    for char in data:
        ascii_val=ord(char)
        binary=format(ascii_val,' 08b')
        bin_list.append("0"+str(binary)[1:])
    bin_str=''.join(bin_list)
    bin_str+=EOF_marker
    
    if len(bin_str)>len(samples):
        print("Audio file is too small to store this data")
        if args.verbose:
            print("Aborting...")
        sys.exit(1)
    new_samples=np.copy(samples)
    k=0
    for char in bin_str:
        if char=='1':
            if new_samples[k]%2==0:
                new_samples[k]+=1
        else:
            if new_samples[k]%2==1:
                new_samples[k]-=1
        k+=1
    new_frames=new_samples.tobytes()
    output_file_name=input("Enter the name of the output audio file(.wav): ")
    output_path="/home/yuvaganesh/Music/embedded_audio/"+output_file_name
    with wave.open(output_path,"wb") as out:
        out.setparams(params)
        out.writeframes(new_frames)

