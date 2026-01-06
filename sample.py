import subprocess
import os

def extract_keyframes(video_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-framerate", "30",
        "-i","/home/yuvaganesh/StegoScope/tmpikfdir" ,
       "-map", " 0:v:0", "-map", "1:a?",
       "-c:v", "libx264", "-pix_fmt yuv420p",
       stego_video.mp4
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

extract_keyframes()
