import numpy as np 

class Recosntruction:
    def __init__(self,time_before_sampling,time_samples,x_samples,T_s,reconstruction_type):
        self.time_before_sampling=time_before_sampling
        self.time_samples=time_samples
        self.x_samples=x_samples
        self.T_s=T_s
        self.reconstruction_type=reconstruction_type
    

    def whittaker_shannon_reconstruction(self):
        sinc_matrix = np.sinc((self.time_before_sampling[:, None] - self.time_samples) / self.T_s)
        return np.dot(sinc_matrix, self.x_samples)
    

    
