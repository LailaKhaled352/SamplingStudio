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
        self.plot_time_domain(graph, self.sampled_time, self.sampled_data, signal)
         #self.plot_frequency_domain()

    def plot_time_domain(self,graph,sampled_time,sampled_data,signal):
        
        graph.clear_signal()  # Clear previous plots
        # Plot original signal
 
        graph.set_signal(signal.signal_data_time, signal.signal_data_amplitude)
            
        # Plot sampled signal as points 
        scatter_plot = pg.ScatterPlotItem(
            x=sampled_time, 
            y=sampled_data, 
            pen='r', 
            symbol='x', 
            size=10
        )
        graph.graphWidget.addItem(scatter_plot)  # Access the PlotWidget to add the scatter plot
        print('plotting function')
    # def plot_frequency_domain(self):
    # Perform FFT on the sampled data
     # fft_result = np.fft.fft(self.sampled_data)
    #  freqs = np.fft.fftfreq(len(fft_result), self.sampling_interval)
    #  magnitude = np.abs(fft_result)

    # Clear previous plots
    #  self.graph_freq.clear()

    # Plot the original frequency components as scatter points
    #  scatter_plot = pg.ScatterPlotItem(
      #   x=freqs, 
      #   y=magnitude, 
      #   pen=None, 
      #   symbol='o', 
      #   size=5, 
      #   brush='g'
    # )
    #  self.graph_freq.addItem(scatter_plot)

    # Only show aliasing effects if sampling frequency < 2 * max frequency
      #sample_rate = (
      #   self.get_actual_sampling_frequency()
      #   if self.sampling_mode == 0
      #   else self.get_normalized_sampling_frequency()
    # )
     # if sample_rate < 2 * self.max_freq:
        # Set up arrays for aliasing visualization
      #   repeated_freqs = []
       #  repeated_magnitudes = []

        # Number of repetitions to account for aliasing
        # num_repeats = int(np.ceil((2 * self.max_freq) / sample_rate)) + 1

        # Repeat the spectrum to show aliasing at different harmonics
       #  for i in range(-num_repeats, num_repeats + 1):
          #   repeated_freqs.extend(freqs + i * sample_rate)
            # repeated_magnitudes.extend(magnitude)

        # Convert lists to numpy arrays for plotting
        # repeated_freqs = np.array(repeated_freqs)
       #  repeated_magnitudes = np.array(repeated_magnitudes)

        # Plot aliased frequencies without connecting lines
        # aliased_plot = pg.ScatterPlotItem(
          #   x=repeated_freqs,
          #   y=repeated_magnitudes,
          #   pen=None,
          #   symbol='x',
           #  size=5,
          #   brush='r'
        # )
        # self.graph_freq.addItem(aliased_plot)
        
    # def update_frequency_display(self):
      #   if self.freqModeActual.isChecked():
       #      self.sampling_mode = 0
            # Set the slider range to 0 to 4*f_max, stepping by 1 Hz
       #      self.sampleSlider.setMinimum(1)
       #      self.sampleSlider.setMaximum(int(4 * self.max_freq))
       #      self.sampleSlider.setSingleStep(1)
       #      self.sampleSlider.setValue(int(2 * self.max_freq))  # Default to 2 * f_max
          #else:
       #      self.sampling_mode = 1
            # Set the slider range to f_max, 2*f_max, 3*f_max, and 4*f_max, stepping by f_max
       #      self.sampleSlider.setMinimum(1)
       #      self.sampleSlider.setMaximum(4)
       #      self.sampleSlider.setSingleStep(1)
       #      self.sampleSlider.setValue(1)  # Default to 1 * f_max
       #  self.update_freq_label(self.freqLabel)
       #  self.update_sampling()

   
