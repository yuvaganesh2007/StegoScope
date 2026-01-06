import numpy as np
from PIL import Image
from steganalysis.core.base import StegPlugin

class RSAnalysis(StegPlugin):
    name = "rs_analysis"
    media_type = "image"

    def smoothness(self, block):
        return np.sum(np.abs(np.diff(block)))

    def analyze(self, path):
        img = Image.open(path).convert("L")
        pixels = np.array(img).flatten()

        block_size = 4
        R = S = 0

        for i in range(0, len(pixels) - block_size, block_size):
            block = pixels[i:i + block_size]
            s1 = self.smoothness(block)

            flipped = block ^ 1
            s2 = self.smoothness(flipped)

            if s2 > s1:
                R += 1
            elif s2 < s1:
                S += 1

        diff = abs(R - S)

        return {
            "suspicious": diff < 100
        }

