#!/usr/bin/env python3

import wave
import numpy as np
import matplotlib

audio=wave.open("/home/yuvaganesh/Music/audiosample.wav")

array=audio.readframes(-1)
num_arr=np.frombuffer(array, dtype=np.int16)
#new_num_arr=num_arr.copy()
print(audio.getsampwidth())
print(num_arr[0])
print(len(num_arr))

