import wave
import numpy as np
from steganalysis.core.base import StegPlugin

class AudioLSB(StegPlugin):
    name = "audio_lsb"
    media_type = "audio"

    def analyze(self, path):
        with wave.open(path, 'rb') as wf:
            frames = wf.readframes(-1)

        samples = np.frombuffer(frames, dtype=np.int16)
        lsb = samples & 1

        return {
            "suspicious": abs(np.mean(lsb) - 0.5) < 0.05
        }       
