import numpy as np
import math
class Sinusoid:
    def __init__(self, freq, amp, phase):
        self.freq= freq
        self.amp= amp
        self.phase =phase
        self.sinusoid = None

    def generate_sinusoid(self, x_window):
        self.sinusoid= self.amp* np.sin(2*math.pi*self.freq*x_window)
        return  self.sinusoid


        