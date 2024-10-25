from PyQt5.QtWidgets import QColorDialog, QPushButton, QMainWindow
from PyQt5.QtGui import QColor,QBrush
import pandas as pd
import numpy as np


class Signal:
    def __init__(self, graph_num,csv_path):
        self.csv_path = csv_path
        csvFile = pd.read_csv(self.csv_path)   
        self.signal_data_time = csvFile.iloc[:, 0].values
        self.signal_data_amplitude = csvFile.iloc[:, 1].values
        self.graph_num= graph_num
        

   
    

    def add_noise(self, SNR):
        signal_power=np.mean((self.signal_data_amplitude)**2)
        SNR_linear = 10**(SNR/10)
        noise_power = signal_power/SNR_linear
        noise = np.random.normal(0,np.sqrt(noise_power),self.signal_data_amplitude.shape)
        noisy_signal = self.signal_data_amplitude + noise
        return noisy_signal

    
    
    def set_signal_graph_num(self, new_graph_num):
        self.graph_num = new_graph_num

    def get_signal_graph_num(self):
        return self.graph_num    

        
