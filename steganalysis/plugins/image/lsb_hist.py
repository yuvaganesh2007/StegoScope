import numpy as np
from PIL import Image
from steganalysis.core.base import StegPlugin

class LSBHistogram(StegPlugin):
    name = "lsb_histogram"
    media_type = "image"

    def analyze(self, path):
        img = Image.open(path).convert("RGB")
        arr = np.array(img).reshape(-1)

        lsb = arr & 1
        zeros = np.sum(lsb == 0)
        ones = np.sum(lsb == 1)

        ratio = abs(zeros - ones) / len(lsb)

        return {
            "suspicious": ratio > 0.050
        } 
