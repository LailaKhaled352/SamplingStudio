import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.interpolate import CubicSpline

# Define parameters
f_max = 5  # Maximum frequency for the original signal
f_s = 2 * 2 * f_max  # Sampling frequency (Nyquist rate)
T_s = 1 / f_s  # Sampling interval
time_range = np.linspace(-1, 1, 1000)  # Continuous time for plotting

# Original Signal
def original_signal(t):
    return (
        np.sin(2 * np.pi * f_max * t) +
        0.5 * np.sin(2 * np.pi * (f_max / 2) * t) +
        0.3 * np.sin(2 * np.pi * (f_max / 3) * t) +
        0.2 * np.sin(2 * np.pi * (f_max * 1.5) * t) +
        0.1 * np.sin(2 * np.pi * (f_max * 2) * t)
    )

# Sampling Function
def sampled_signal(f_s, noise_level=0):
    np.random.seed(0)  # Set a fixed random seed for reproducibility
    t_samples = np.arange(-1, 1, 1 / f_s)
    x_samples = original_signal(t_samples)
    noise = np.random.normal(0, noise_level, len(x_samples))
    # x_samples += noise  # Uncomment if noise is desired
    return t_samples, x_samples

# Reconstruction Functions
def sinc_reconstruction(t, t_samples, x_samples, T_s):
    sinc_matrix = np.sinc((t[:, None] - t_samples) / T_s)
    return np.dot(sinc_matrix, x_samples)

def zero_order_hold_interpolation(t, t_samples, x_samples):
    interpolated_values = np.zeros_like(t)
    for i in range(len(t)):
        idx = np.searchsorted(t_samples, t[i]) - 1
        if idx < 0:
            interpolated_values[i] = x_samples[0]
        elif idx >= len(x_samples) - 1:
            interpolated_values[i] = x_samples[-1]
        else:
            interpolated_values[i] = x_samples[idx]
    return interpolated_values

def cubic_spline_reconstruction(t, t_samples, x_samples):
    cs = CubicSpline(t_samples, x_samples)
    return cs(t)

def fourier_interpolation(t, t_samples, x_samples):
    # Number of samples
    n = len(x_samples)
    
    # Perform FFT
    X_f = np.fft.fft(x_samples)
    
    # Frequency bins
    freq = np.fft.fftfreq(n, d=1/f_s)
    
    # Create a mask to retain frequencies within the Nyquist limit
    mask = np.abs(freq) <= f_max
    
    # Inverse FFT to reconstruct signal
    X_f_filtered = np.zeros_like(X_f)
    X_f_filtered[mask] = X_f[mask]
    reconstructed_signal = np.fft.ifft(X_f_filtered)

    # Interpolate to the desired time range
    return np.interp(t, t_samples, reconstructed_signal.real)

# Generate Sampled Data with Noise
t_samples, x_samples = sampled_signal(f_s, noise_level=0.1)

# Reconstruction
reconstructed_sinc = sinc_reconstruction(time_range, t_samples, x_samples, T_s)
reconstructed_zo = zero_order_hold_interpolation(time_range, t_samples, x_samples)
reconstructed_cubic_spline = cubic_spline_reconstruction(time_range, t_samples, x_samples)
reconstructed_fourier = fourier_interpolation(time_range, t_samples, x_samples)

# Plotting
plt.figure(figsize=(12, 12))

# Original and Sampled Signal
plt.subplot(5, 1, 1)
plt.plot(time_range, original_signal(time_range), label="Original Signal", color="blue")
plt.stem(t_samples, x_samples, label="Sampled Points", linefmt="r-", markerfmt="ro", basefmt=" ")
plt.title("Original Signal and Sampled Points")
plt.legend()

# Whittaker-Shannon Reconstruction
plt.subplot(5, 1, 2)
plt.plot(time_range, reconstructed_sinc, label="Sinc Reconstruction", color="green", linestyle="--")
plt.title("Whittaker-Shannon (Sinc) Reconstruction")
plt.legend()

# Piecewise Constant Interpolation
plt.subplot(5, 1, 3)
plt.plot(time_range, reconstructed_zo, label="Zero-Order Hold", linestyle="--", color="orange")
plt.title("Zero-Order Hold Interpolation")
plt.legend()

# Cubic Spline Reconstruction
plt.subplot(5, 1, 4)
plt.plot(time_range, reconstructed_cubic_spline, label="Cubic Spline Interpolation", linestyle="--", color="purple")
plt.title("Cubic Spline Interpolation")
plt.legend()

# Fourier-Based Reconstruction
plt.subplot(5, 1, 5)
plt.plot(time_range, reconstructed_fourier, label="Fourier-Based Interpolation", linestyle="--", color="brown")
plt.title("Fourier-Based Interpolation")
plt.legend()

plt.tight_layout()
plt.show()

