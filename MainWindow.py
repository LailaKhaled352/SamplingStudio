from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QListWidget ,QSpinBox, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QCursor,QBrush
from PyQt5.QtCore import QPoint
import sys
import pyqtgraph as pg
from Graph import Graph
from Signal import Signal
from Load import Load
from ComposedSignal import ComposedSignal
import numpy as np
from sampling import SamplingClass
import os 
from Reconstruction import Recosntruction
import numpy as np 
import pywt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("SamplingStudio.ui", self)
        self.setWindowTitle("Sampling Studio")
        self.signal=None
        self.composed_signal_instance= ComposedSignal()
        self.sample=SamplingClass()
        self.reconstruct=None

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
        self.sampleSlider.valueChanged.connect(self.update_sampling_freq)
        
        # Connect upload signal button
        self.upload_button = self.findChild(QWidget, 'uploadButton_2')
        self.upload_button.clicked.connect(self.load_signal)

         # Connect remove file button
        self.remove_button = self.findChild(QPushButton, 'uploadButton')
        self.remove_button.clicked.connect(self.clear_signals)

        self.load_instance = Load()  # Instance of the Load class
        
        #Fatma
        self.add_component_button= self.findChild(QPushButton, 'addComponent')
        self.frequency_entry= self.findChild(QSpinBox, 'freqSpinBox')
        self.phase_entry= self.findChild(QSpinBox, 'phaseSpinBox')
        self.amplitude_entry= self.findChild(QSpinBox, 'ampSpinBox')
        self.frequency_entry.setValue(1)
        self.phase_entry.setValue(0)
        self.amplitude_entry.setValue(1)
        self.add_component_button.clicked.connect(self.add_component)

        self.signals_List = self.findChild(QListWidget, 'signalsList')
        self.components_List = self.findChild(QListWidget, 'componList')
        self.attr_List = self.findChild(QListWidget, 'attrList')

        self.save_signal_button= self.findChild(QPushButton, 'GenerateButton')
        self.save_signal_button.clicked.connect(self.save_signal)

        # Initial configuration
        # self.update_frequency_mode()

        # Judy

        # noise connected
        self.noise_slider = self.findChild(QSlider, 'noiseSlider')
        self.noise_slider.setRange(1, 30) 
        self.noise_slider.setValue(30)
        self.noise_slider.valueChanged.connect(self.update_noise) 
        
        # reconstruction connected 
        self.reconstruction_method = self.findChild(QComboBox, 'reconstructon_combobox')
        self.rec_method = "Whittaker-Shannon"
        self.reconstruction_method.currentIndexChanged.connect(self.handle_combobox_change)
        # self.plot_recosntruction()


        self.sampled_time=None
        self.sampled_data=None

    

    def plot_recosntruction(self):
        if self.signal is not None:
            self.reconstruct.update_recosntruction(self.graph2,self.signal.signal_data_time,self.sample.sampled_time,self.sample.sampled_data,self.sample.sampling_interval,self.rec_method)


    def handle_combobox_change(self, index):
        self.rec_method = self.reconstruction_method.currentText()

    def update_sampling_freq(self):
        if self.signal is not None:
            self.update_sampling_frequency(self.signal.signal_data_amplitude)      
            


    def update_frequency_mode(self):

        if self.actualRadio.isChecked():
            # Set slider for actual frequency mode
            print('enter mode')
            # max_frequency = int(4 * self.sample.max_freq)
            print({self.sample.max_freq})
            self.sampleSlider.setRange(0, 4 * self.sample.max_freq)
            self.sampleSlider.setSingleStep(self.sample.max_freq)
            self.sampleSlider.setValue(int(2 * self.sample.max_freq))  # Start at 2*f_max
            self.sample.sampling_mode = 0
        if self.normalRadio.isChecked():
            # Set slider for normalized frequency mode
            self.sampleSlider.setRange(1, 4)
            self.sampleSlider.setSingleStep(1)
            self.sampleSlider.setValue(1)  # Start at 1 * f_max
            self.sample.sampling_mode = 1
   
      # Immediately update sampling frequency based on new slider value
        if self.signal is not None:
            self.update_sampling_frequency(self.signal.signal_data_amplitude)

    def update_sampling_frequency(self,signal_data_amplitude):
            
        if self.sample.sampling_mode == 0:
            # Actual mode - slider directly reflects sampling frequency in Hz
            print(self.sampleSlider.value())
            self.sample_rate = max(self.sampleSlider.value(), 1) 
            print('division b')
        if self.sample.sampling_mode == 1:

            # Normalized mode - slider value is a multiplier for f_max
           self.sample_rate = max(self.sampleSlider.value() * self.sample.max_freq, 1)

        # Update the sampling in SamplingClass
        self.sample.sampling_interval = 1 / self.sample_rate
        
        if self.signal is not None:  # Ensure a signal is loaded
            self.sample.update_sampling( self.graph1,self.signal.signal_data_time,signal_data_amplitude,self.sample_rate,self.signal)
            self.plot_recosntruction()

  
    # Judy 
    def update_noise(self):
        self.graph1.clear_signal()
        updated_signal_data_amplitude =self.signal.add_noise(self.noise_slider.value())
        self.update_sampling_frequency(updated_signal_data_amplitude)
        self.plot_recosntruction()
        
     
    #Fatma
    def add_component(self):
        freq= self.frequency_entry.value() 
        amp=self.amplitude_entry.value()
        phase=np.deg2rad(self.phase_entry.value())
        self.composed_signal_instance.add_component(freq=freq, amp=amp, phase=phase,attr_list=self.attr_List)
    
    def save_signal(self):
        self.attr_List.clear()
        self.composed_signal_instance.save_signal(self.signals_List) #save this current instance
        self.composed_signal_instance= ComposedSignal() #create a new instance to use here for next added components

    def create_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("""
        QMenu {
            color: white;  /* Default text color */
        }
        QMenu::item::selected {  /* Hover state */
            color: black;  /* Text color when hovering */
            background-color: #a5a5a5;  /* Optional background color on hover */
        } """)

        if self.signals_List.underMouse():
            signals_List_widget = self.signals_List
            selected_row = signals_List_widget.selectionModel().currentIndex().row()
            remove_signal_action = context_menu.addAction("Remove Signal")
            remove_signal_action.triggered.connect(lambda: ComposedSignal.remove_signal(signals_List_widget, selected_row))

            show_components_action = context_menu.addAction("Show Components")
            show_components_action.triggered.connect(lambda: ComposedSignal.show_components(self.components_List, selected_row))

            
            load_signal_action = context_menu.addAction("Load Signal")
            load_signal_action.triggered.connect(lambda: self.load_composed_signal(selected_row))
        
        elif self.components_List.underMouse():
            components_list_widget= self.components_List
            selected_row = components_list_widget.selectionModel().currentIndex().row() 
            remove_component_action = context_menu.addAction("Remove Component")
            remove_component_action.triggered.connect(lambda: ComposedSignal.remove_component(components_list_widget, selected_row))
        else:
            return         
 
        # Get the global position of the cursor
        cursor_position = QCursor.pos()
        context_menu.exec_(cursor_position)

    
    def contextMenuEvent(self, event):
        self.create_context_menu(event.pos())

    def load_composed_signal(self, index):
        selected_signal= ComposedSignal.composed_signals_list[index]
        self.sample_rate = self.sampleSlider.value()
        self.sample.max_freq= selected_signal.get_max_freq()
        path= selected_signal.to_csv()
        self.signal = Signal(graph_num=1, csv_path=path)

        sampled_time, sampled_data =self.sample.sample_signal(self.signal.signal_data_time,self.signal.signal_data_amplitude,self.sample_rate)
        self.sample.plot_time_domain(self.graph1,sampled_time,sampled_data,self.signal.signal_data_time,self.signal.signal_data_amplitude)
        self.reconstruct=Recosntruction(self.signal.signal_data_time,self.sample.sampled_time,self.sample.sampled_data,self.reconstruction_method.currentText())
        #self.graph1.set_signal(self.signal.signal_data_time, self.signal.signal_data_amplitude)
        self.plot_recosntruction()
       
   
    def show_default(self):
        print('first 11')

        self.signal = Signal(graph_num=1)
         # Get the sample rate from the slider
        self.sample_rate = self.sampleSlider.value()
        self.sample.max_freq=self.sample.get_max_freq(self.signal.signal_data_time, self.signal.signal_data_amplitude)
    
        self.sampled_time, self.sampled_data =self.sample.sample_signal(self.signal.signal_data_time,self.signal.signal_data_amplitude,self.sample_rate)
        print('first')
        self.sample.plot_time_domain(self.graph1,self.sampled_time,self.sampled_data,self.signal.signal_data_time,self.signal.signal_data_amplitude)
        print('second')

        self.reconstruct=Recosntruction(self.signal.signal_data_time,self.sample.sampled_time,self.sample.sampled_data,self.sample.sampling_interval,self.rec_method)
        self.plot_recosntruction()
    
    def load_signal(self):
        file_path = self.load_instance.browse_signals()
        if file_path:
            self.signal = Signal(graph_num=1, csv_path=file_path)
            self.graph1.set_signal(self.signal.signal_data_time, self.signal.signal_data_amplitude)
            self.update_sampling_frequency(self.signal.signal_data_amplitude)

    def clear_signals(self):
        self.graph1.clear_signal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show_default()
    window.show()
    sys.exit(app.exec_()) 