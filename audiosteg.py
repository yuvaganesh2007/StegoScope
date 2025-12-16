import wave
import numpy as np
import argparse
import sys 

parser=argparse.ArgumentParser()

parser.add_argument("file", help="image file to handle")
parser.add_argument("--extract","-e", action="store_true", help="choose to extract")
parser.add_argument("--embed", "-E", action="store_true", help="to embed data into the file")
group=parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args=parser.parse_args()

audio=wave.open(args.path)
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

print(type(samples))
print(samples[0])
