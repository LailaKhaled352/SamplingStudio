from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QCursor,QBrush
from PyQt5.QtCore import QPoint
import sys
import pyqtgraph as pg
from Graph import Graph
from Signal import Signal
from Load import Load

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("SamplingStudio.ui", self)

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

    def show_default(self):
        signal = Signal(graph_num=1)
        self.graph1.set_signal(signal.signal_data_time, signal.signal_data_amplitude)
    
    def load_signal(self):
        file_path = self.load_instance.browse_signals()
        if file_path:
            signal = Signal(graph_num=1, csv_path=file_path)
            self.graph1.set_signal(signal.signal_data_time, signal.signal_data_amplitude)

    def remove_signal(self):
        self.graph1.clear_signal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show_default()
    window.show()
    sys.exit(app.exec_()) 