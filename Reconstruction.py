import numpy as np 
import pywt
import cvxpy as cp
class Recosntruction:
    def __init__(self,time_before_sampling,time_samples,x_samples,T_s,reconstruction_type):
        self.time_before_sampling=time_before_sampling
        self.time_samples=time_samples
        self.x_samples=x_samples
        self.T_s=T_s
        self.reconstruction_type=reconstruction_type
        # until sampling is done 
        self.f_max = 10   
        self.f_s = 20     
        self.T_s = 1 / self.f_s  
        self.time_range = np.linspace(-1, 1, 1000)          

    def recons_method(self):
        if self.reconstruction_type == "Whittaker-Shannon":
            return self.whittaker_shannon_reconstruction()

        elif self.reconstruction_type == "Wavelet":
            return self.wavelet_reconstruction()

        else:
            return self.zero_order_hold_interpolation()
        
    def update_recosntruction(self,graph2,time_before_sampling,time_samples,x_samples,T_s,reconstruction_type):
        print("reconstruction1")
        self.time_before_sampling=time_before_sampling
        self.time_samples=time_samples
        self.x_samples=x_samples
        self.T_s=T_s
        self.reconstruction_type=reconstruction_type
        graph2.clear_signal()
        graph2.set_signal(self.time_before_sampling, self.recons_method())
        print("reconstruction2")
        return self.recons_method() 
    
       
    def whittaker_shannon_reconstruction(self):
        print("reconstruction3")
        sinc_matrix = np.sinc((self.time_before_sampling[:, None] - self.time_samples) / self.T_s)
        return np.dot(sinc_matrix, self.x_samples)
    

    def wavelet_reconstruction(self, wavelet='db1'):
    
        coeffs = pywt.wavedec(self.x_samples, wavelet)
        reconstructed_signal = pywt.waverec(coeffs, wavelet)
        return np.interp(self.time_before_sampling, np.linspace(self.time_samples[0], self.time_samples[-1], len(reconstructed_signal)), reconstructed_signal)

    
    def zero_order_hold_interpolation(self):
        interpolated_values = np.zeros_like(self.time_before_sampling)
        for i in range(len(self.time_before_sampling)):
            idx = np.searchsorted(self.time_samples, self.time_before_sampling[i]) - 1
            if idx < 0:
                interpolated_values[i] = self.x_samples[0]
            elif idx >= len(self.x_samples) - 1:
                interpolated_values[i] = self.x_samples[-1]
            else:
                interpolated_values[i] = self.x_samples[idx]
        return interpolated_values