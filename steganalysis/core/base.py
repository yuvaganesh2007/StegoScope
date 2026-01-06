from abc import ABC, abstractmethod

class StegPlugin(ABC):
    name = "base"
    media_type = None  # image / audio / video

    @abstractmethod
    def analyze(self, path):
        pass
