#!/usr/bin/env python3

with open("/home/yuvaganesh/Pictures/123.xyz", "rb") as file:
    data= file.read(16)

    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        print("PNG Image")
    if data.startswith(b'\xFF\xD8\xFF'):
        print("JPEG Image")
    if data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
        print("GIF Image")
    if data.startswith(b'BM'):
        print("BMP Image")
