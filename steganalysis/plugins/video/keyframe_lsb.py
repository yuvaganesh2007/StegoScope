import subprocess
import numpy as np
from PIL import Image
from steganalysis.core.base import StegPlugin
import os

class VideoKeyframeLSB(StegPlugin):
    name = "video_keyframe_lsb"
    media_type = "video"
    os.system("mkdir /home/yuvaganesh/newtmpdir")
    def analyze(self, path):
        subprocess.run(
            ["ffmpeg", "-skip_frame", "nokey", "-i", path, "/home/yuvaganesh/newtmpdir/tmp_kf_%03d.png"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        bits = []
        for i in range(1, 4):
            img = Image.open(f"/home/yuvaganesh/newtmpdir/tmp_kf_{i:03d}.png").convert("RGB")
            arr = np.array(img).reshape(-1)
            bits.extend(arr & 1)
        os.system("rm -r /home/yuvaganesh/newtmpdir")
        return {
            "suspicious": abs(np.mean(bits) - 0.5) < 0.05
        }
        
