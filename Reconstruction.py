import numpy as np 
import pywt
class Recosntruction:
    def __init__(self,time_before_sampling,time_samples,x_samples,T_s,reconstruction_type="Whittaker-Shannon"):
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
            return self.spectral_extrapolation()
        
    def update_recosntruction(self,time_before_sampling,time_samples,x_samples,T_s,reconstruction_type):
        print("reconstruction1")
        self.time_before_sampling=time_before_sampling
        self.time_samples=time_samples
        self.x_samples=x_samples
        self.T_s=T_s
        self.reconstruction_type=reconstruction_type
        print("reconstruction2")
    
       
    def whittaker_shannon_reconstruction(self):
        print("reconstruction3")
        sinc_matrix = np.sinc((self.time_before_sampling[:, None] - self.time_samples) / self.T_s)
        return np.dot(sinc_matrix, self.x_samples)
    

    def wavelet_reconstruction(self, wavelet='db1'):
    
        coeffs = pywt.wavedec(self.x_samples, wavelet)
        reconstructed_signal = pywt.waverec(coeffs, wavelet)
        return np.interp(self.time_before_sampling, np.linspace(self.time_samples[0], self.time_samples[-1], len(reconstructed_signal)), reconstructed_signal)

    
    def spectral_extrapolation(self, extrapolation_factor=2):
    
        X_f = np.fft.fft(self.x_samples)
        n = len(X_f)
        X_f_extrapolated = np.zeros(extrapolation_factor * n, dtype=complex)
        X_f_extrapolated[:n//2] = X_f[:n//2]  
        X_f_extrapolated[-n//2:] = X_f[-n//2:]   
        extended_signal = np.fft.ifft(X_f_extrapolated).real
        t_extended = np.linspace(self.time_samples[0], self.time_samples[-1], len(extended_signal))
        return np.interp(self.time_before_sampling, t_extended, extended_signal)