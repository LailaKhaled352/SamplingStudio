from Sinusoid import Sinusoid
import numpy as np
class Composer:
    def __init__(self):
        self.sinusoidals_list= []
        self.composed_signal= None
        self.composed_signals=[]
    

    def add_component(self, freq, amp, phase, x_window):
        sinusoid= Sinusoid(freq, amp, phase)
        sinusoid_generated= sinusoid.generate_sinusoid(x_window)
        self.sinusoidals_list.append(sinusoid_generated)
        print(self.sinusoidals_list)
        self.compose_signal()
    
    def compose_signal(self):
        self.composed_signal= np.sum(self.sinusoidals_list, axis=0)
    
    def save_signal(self):
        self.composed_signals.append(self.composed_signal)

    def remove_componet(self, index):
        _=self.sinusoidals_list.pop(index)
        self.compose_signal()

"""if __name__ =='__main__':
    composer= Composer()
    x_window= np.linspace(0,20,100)
    composer.add_component(4,1,0, x_window)
    composer.compose_signal()
    composed_signal= composer.composed_signal
    print(composed_signal)"""