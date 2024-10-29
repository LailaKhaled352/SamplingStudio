import numpy as np
import pyqtgraph as pg

class ErrorCalculation:
    def __init__(self, original_signal_time, original_signal_amplitude, reconstructed_signal_amplitude):
        super().__init__()
        self.original_signal_time = original_signal_time
        self.original_signal_amplitude = original_signal_amplitude
        self.reconstructed_signal_amplitude = reconstructed_signal_amplitude
        self.error_signal = None

    def calculate_error(self):
        # Ensure both signals are of the same length
        min_length = min(len(self.original_signal_amplitude), len(self.reconstructed_signal_amplitude))
        self.original_signal_amplitude = self.original_signal_amplitude[:min_length]
        self.reconstructed_signal_amplitude = self.reconstructed_signal_amplitude[:min_length]
        self.original_signal_time = self.original_signal_time[:min_length]

        # Calculate the error signal
        self.error_signal = self.original_signal_amplitude - self.reconstructed_signal_amplitude
        

    def plot_error(self, graph):
        graph.clear_signal()
        graph.set_signal(self.original_signal_time, self.error_signal)