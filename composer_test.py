import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QSpinBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Sinusoid import Sinusoid
from Composer import Composer

class SignalMixerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up Composer instance
        self.composer = Composer()
        
        # Set up time window for the sinusoids
        self.x_window = np.linspace(0,5 , 100)

        # Set up main window
        self.setWindowTitle("Signal Mixer")
        self.setGeometry(200, 200, 800, 600)
        
        # Set up central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Control panel for adding components
        control_panel = QHBoxLayout()

        self.freq_spinbox = QSpinBox()
        self.freq_spinbox.setRange(1, 20)
        self.freq_spinbox.setValue(1)
        control_panel.addWidget(QLabel("Frequency (Hz):"))
        control_panel.addWidget(self.freq_spinbox)

        self.amp_spinbox = QSpinBox()
        self.amp_spinbox.setRange(1, 10)
        self.amp_spinbox.setValue(1)
        control_panel.addWidget(QLabel("Amplitude:"))
        control_panel.addWidget(self.amp_spinbox)

        self.phase_spinbox = QSpinBox()
        self.phase_spinbox.setRange(0, 360)
        self.phase_spinbox.setValue(0)
        control_panel.addWidget(QLabel("Phase (degrees):"))
        control_panel.addWidget(self.phase_spinbox)

        add_component_button = QPushButton("Add Component")
        add_component_button.clicked.connect(self.add_component)
        control_panel.addWidget(add_component_button)


        layout.addLayout(control_panel)

    def add_component(self):
        freq = self.freq_spinbox.value()
        amp = self.amp_spinbox.value()
        phase = np.deg2rad(self.phase_spinbox.value())
        self.composer.add_component(freq, amp, phase, self.x_window)
        self.update_plot()

    def update_plot(self):
        self.composer.compose_signal()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(self.x_window, self.composer.composed_signal)
        ax.set_title("Composed Signal")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalMixerApp()
    window.show()
    sys.exit(app.exec_())
