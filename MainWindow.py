from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QCursor,QBrush
from PyQt5.QtCore import QPoint
import sys
import pyqtgraph as pg
from Graph import Graph
from Signal import Signal
from Load import Load
from sampling import SamplingClass
import os 
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("SamplingStudio.ui", self)
        self.signal=None
        self.sample=SamplingClass()

        #Laila
            # Initialize the existing PlotWidget
        self.graph1 = self.findChild(pg.PlotWidget, 'graph1_2')
        self.graph2 = self.findChild(pg.PlotWidget, 'graph1')
        self.graph3 = self.findChild(pg.PlotWidget, 'graph2')
        self.graph4 = self.findChild(pg.PlotWidget, 'graph3')

        # Create an instances of the Graph class for graph 1, 2, 3, 4
        self.graph1 = Graph(self.graph1, "Graph 1", "Time", "Amplitude")
        self.graph2 = Graph(self.graph2, "Graph 2", "Time", "Amplitude")
        self.graph3 = Graph(self.graph3, "Graph 3", "Time", "Amplitude")
        self.graph4 = Graph(self.graph4, "Graph 4", "Frequency", "Amplitude")
         #hajar
        self.sample_rate=1
         # Find the slider and radio buttons
        self.sampleSlider = self.findChild(QSlider, 'sampleSlider')
        self.sampleSlider.setMinimum(1)
        self.actualRadio = self.findChild(QRadioButton, 'actualRadio')
        self.normalRadio = self.findChild(QRadioButton, 'normalRadio')

         # Set up connections for slider and radio buttons
        self.actualRadio.toggled.connect(self.update_frequency_mode)
        self.normalRadio.toggled.connect(self.update_frequency_mode)
        self.sampleSlider.valueChanged.connect(self.update_sampling_frequency)
        
        # Connect upload signal button
        self.upload_button = self.findChild(QWidget, 'uploadButton_2')
        self.upload_button.clicked.connect(self.load_signal)

         # Connect remove file button
        self.remove_button = self.findChild(QPushButton, 'uploadButton')
        self.remove_button.clicked.connect(self.clear_signals)

        self.load_instance = Load()  # Instance of the Load class
        # Initial configuration
        self.update_frequency_mode()

    def update_frequency_mode(self):
        if self.actualRadio.isChecked():
            # Set slider for actual frequency mode
            print('enter mode')
            max_frequency = int(4 * self.sample.max_freq)
            print({self.sample.max_freq})
            self.sampleSlider.setRange(1, max_frequency)
            self.sampleSlider.setSingleStep(1)
            self.sampleSlider.setValue(int(2 * self.sample.max_freq))  # Start at 2*f_max
            self.sample.sampling_mode = 0
        if self.normalRadio.isChecked():
            # Set slider for normalized frequency mode
            self.sampleSlider.setRange(1, 4)
            self.sampleSlider.setSingleStep(1)
            self.sampleSlider.setValue(1)  # Start at 1 * f_max
            self.sample.sampling_mode = 1
   
      # Immediately update sampling frequency based on new slider value
        self.update_sampling_frequency()

    def update_sampling_frequency(self):
        if self.sample.sampling_mode == 0:
            # Actual mode - slider directly reflects sampling frequency in Hz
            self.sample_rate = max(self.sampleSlider.value(), 1) 
            print('division b')
        if self.sample.sampling_mode == 1:

            # Normalized mode - slider value is a multiplier for f_max
           self. sample_rate = max(self.sampleSlider.value() * self.sample.max_freq, 1)

        # Update the sampling in SamplingClass
        self.sample.sampling_interval = 1 / self.sample_rate
        
        if self.signal is not None:  # Ensure a signal is loaded
         self.sample.update_sampling( self.graph1,self.signal.signal_data_time, self.signal.signal_data_amplitude,self.sample_rate,self.signal)

    def show_default(self):
        print('first 11')

        self.signal = Signal(graph_num=1)
         # Get the sample rate from the slider
        self.sample_rate = self.sampleSlider.value()
        self.sample.max_freq=self.sample.get_max_freq(self.signal.signal_data_time, self.signal.signal_data_amplitude)
    
        sampled_time, sampled_data =self.sample.sample_signal(self.signal.signal_data_time,self.signal.signal_data_amplitude,self.sample_rate)
        print('first')
        self.sample.plot_time_domain(self.graph1,sampled_time,sampled_data,self.signal)
        print('second')


    
    def load_signal(self):
        file_path = self.load_instance.browse_signals()
        if file_path:
            self.signal = Signal(graph_num=1, csv_path=file_path)
            self.graph1.set_signal(self.signal.signal_data_time, self.signal.signal_data_amplitude)
            self.update_sampling_frequency()
    def remove_signal(self):
        self.graph1.clear_signal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show_default()
    window.show()
    sys.exit(app.exec_()) 