import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget

class Graph:
    def __init__(self, graphWidget, title):
        self.title = title
        self.graphWidget = graphWidget

        # Ensure the parent widget has a layout
        if graphWidget.layout() is None:
            layout = QVBoxLayout(graphWidget)
            graphWidget.setLayout(layout)
        else:
            layout = graphWidget.layout()
        layout.addWidget(self.graphWidget)

        
        #colors
        # Set background and grid
        self.graphWidget.setBackground('#0c202a')
    

        # Configure plot labels and axis colors
        self.graphWidget.getAxis('left').setPen('w')
        self.graphWidget.getAxis('bottom').setPen('w')
        self.graphWidget.getAxis('left').setTextPen('w')
        self.graphWidget.getAxis('bottom').setTextPen('w')
        

        self.signal_plot = self.graphWidget.plot()

        self.signal_x = []
        self.signal_y = []

    def set_signal(self, signal_x, signal_y):
        self.signal_x = signal_x
        self.signal_y = signal_y
        self.graphWidget.plot(self.signal_x, self.signal_y, pen='#3286ad')

    def clear_signal(self):
        self.graphWidget.clear()
        self.signal_x = []
        self.signal_y = []
