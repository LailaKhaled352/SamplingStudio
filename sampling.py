
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class SamplingClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize attributes for sampled data
        self.sampled_time = None
        self.sampled_data = None
        self.sampling_interval = None
        self.sampling_mode = 0  # 0 for actual, 1 for normalized
        self.max_freq=0
     

    

    def get_max_freq(self,signal_data_time, signal_data_amplitude):
    
        fft_result = np.fft.fft(signal_data_amplitude)
        sampling_interval = signal_data_time[1] - signal_data_time[0]
        frequencies = np.fft.fftfreq(len(fft_result), sampling_interval)
        return np.max(np.abs(frequencies))

    def sample_signal(self, signal_data_time,signal_data_amplitude,sample_rate):
        
        self.sampling_interval = 1 / sample_rate
        self.sampled_time = np.arange(0, max(signal_data_time), self.sampling_interval)
        self.sampled_data = np.interp(self.sampled_time, signal_data_time, signal_data_amplitude)

        return self.sampled_time, self.sampled_data

    def update_sampling(self, graph,signal_data_time, signal_data_amplitude,sample_rate,signal):
        self.sampled_time, self.sampled_data = self.sample_signal(signal_data_time, signal_data_amplitude,sample_rate)
        self.plot_time_domain(graph, self.sampled_time, self.sampled_data, signal_data_time, signal_data_amplitude)
         #self.plot_frequency_domain()

    def plot_time_domain(self,graph,sampled_time,sampled_data,signal_data_time, signal_data_amplitude):
        
        graph.clear_signal()  # Clear previous plots
        # Plot original signal
        print(f"signal_data_time[-1] {signal_data_time[-1]}")
        graph.set_signal(signal_data_time,signal_data_amplitude)
            
        # Plot sampled signal as points 
        scatter_plot = pg.ScatterPlotItem(
            x=sampled_time, 
            y=sampled_data, 
            pen='r', 
            symbol='x', 
            size=10
        )
        graph.graphWidget.addItem(scatter_plot)  # Access the PlotWidget to add the scatter plot

    def plot_frequency_domain(self, graph, sample_rate,signal_data_time,signal_data_amplitude):
     if signal_data_amplitude is not None:
        fft_result = np.fft.fft(signal_data_amplitude)
        freqs = np.fft.fftfreq(len(fft_result), (signal_data_time[1] - signal_data_time[0]))
        magnitude = np.abs(fft_result)

        # Clear previous frequency plots
        graph.clear_signal()
    

        # Plot the original frequency spectrum in green
        original_plot = pg.PlotDataItem(
            freqs,
            magnitude,
            pen=pg.mkPen('g', width=6)
        )
        graph.graphWidget.addItem(original_plot)

        graph.graphWidget.setLimits(xMin=-9 * self.max_freq, xMax=9* self.max_freq)
        # Calculate the shift based on the sampling rate
        shift_frequency = sample_rate

        # Plot left and right shifted frequency spectra
        # Left shift
        shifted_freqs_left = freqs - shift_frequency
        left_shifted_plot = pg.PlotDataItem(
            shifted_freqs_left,
            magnitude,
            pen=pg.mkPen('r', width=6, style=pg.QtCore.Qt.DashLine)
        )
        graph.graphWidget.addItem(left_shifted_plot)

        # Right shift
        shifted_freqs_right = freqs + shift_frequency
        right_shifted_plot = pg.PlotDataItem(
            shifted_freqs_right,
            magnitude,
            pen=pg.mkPen('b', width=6, style=pg.QtCore.Qt.DashLine)
        )
        graph.graphWidget.addItem(right_shifted_plot)

       