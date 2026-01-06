import numpy as np
from PIL import Image
from steganalysis.core.base import StegPlugin

class ChiSquareTest(StegPlugin):
    name = "chi_square"
    media_type = "image"

    def analyze(self, path):
        img = Image.open(path).convert("L")  # grayscale
        pixels = np.array(img).flatten()

        observed = np.zeros(256)
        for p in pixels:
            observed[p] += 1

        chi = 0
        for i in range(0, 256, 2):
            expected = (observed[i] + observed[i + 1]) / 2
            if expected > 0:
                chi += ((observed[i] - expected) ** 2) / expected
                chi += ((observed[i + 1] - expected) ** 2) / expected

        return {
            "suspicious": chi < 3000  # heuristic threshold
        }

