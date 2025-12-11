#!/usr/bin/env python3

import os
import sys
import argparse as ap

parser=ap.ArgumentParser()
parser.add_argument("path", help="Path of the file to work on")
parser.add_argument("choice", choices=["extract","embed"], help="Choice to work on file")
parser.add_argument("-c", "--custom", action="store_true", help="Select custom embedding method only for images")

args=parser.parse_args()

if args.choice=="extract":
    if args.path.endswith(".png") or args.path.endswith(".jpeg") or args.path.endswith(".jpg") or args.path.endswith(".bmp"):
        if args.custom:
            os.system(f"python3 imagestegcustom.py {args.path} --extract")
        else:
            os.system(f"python3 imagesteg.py {args.path} --extract")
    elif args.path.endswith(".mp4"):
        os.system("python3 audiosteg.py --extract")
    else: 
        os.system("python3 videosteg.py --extract")

elif args.choice=="embed":
    if args.path.endswith(".png") or args.path.endswith(".jpeg") or args.path.endswith(".jpg") or args.path.endswith(".bmp"):
        if args.custom:
            os.system(f"python3 imagestegcustom.py {args.path} --embed")
        else:
            os.system(f"python3 imagesteg.py {args.path} --embed")
    elif args.path.endswith(".mp4"):
        os.system("python3 audiosteg.py --embed")
    else:
        os.system("python3 videosteg.py --embed")
