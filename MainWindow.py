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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("SamplingStudio.ui", self)
        self.signal=None
        self.composed_signal_instance= ComposedSignal()

        #Laila
            # Initialize the existing PlotWidget
        self.graph1 = self.findChild(pg.PlotWidget, 'graph1_2')
        self.graph2 = self.findChild(pg.PlotWidget, 'graph1')
        self.graph3 = self.findChild(pg.PlotWidget, 'graph2')
        self.graph4 = self.findChild(pg.PlotWidget, 'graph3')

        # Create an instances of the Graph class for graph 1, 2, 3, 4
        self.graph1 = Graph(self.graph1, "Graph 1")
        self.graph2 = Graph(self.graph2, "Graph 2")
        self.graph3 = Graph(self.graph3, "Graph 3")
        self.graph4 = Graph(self.graph4, "Graph 4")

        # Connect upload signal button
        self.upload_button = self.findChild(QWidget, 'uploadButton_2')
        self.upload_button.clicked.connect(self.load_signal)

        # Connect remove file button
        self.remove_button = self.findChild(QPushButton, 'uploadButton')
        self.remove_button.clicked.connect(self.remove_signal)

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
        signal_data_time, signal_data_amplitude= selected_signal.load_composed_signal()
        #Code to be added to show the sampled signal on graph1 
    
    def show_default(self):
        self.signal = Signal(graph_num=1)
        self.graph1.set_signal(self.signal.signal_data_time, self.signal.signal_data_amplitude)
    
    def load_signal(self):
        file_path = self.load_instance.browse_signals()
        if file_path:
            self.signal = Signal(graph_num=1, csv_path=file_path)
            self.graph1.set_signal(self.signal.signal_data_time, self.signal.signal_data_amplitude)

    def remove_signal(self):
        self.graph1.clear_signal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show_default()
    window.show()
    sys.exit(app.exec_()) 