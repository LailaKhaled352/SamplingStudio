from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QCursor,QBrush
from PyQt5.QtCore import QPoint

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("MainWindowUI.ui", self)

    
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

        if self.composed_signals_table.underMouse():
            composed_table = self.composed_signals_table
            selected_row = composed_table.selectionModel().currentIndex().row()
            remove_signal_action = context_menu.addAction("Remove Signal")
            remove_signal_action.triggered.connect(lambda: self.remove_signal(composed_table, selected_row))

            show_components = context_menu.addAction("Show Components")
            show_components.triggered.connect(lambda: self.show_components(composed_table, selected_row))
        
        elif self.components_widget.underMouse():
            components_table= self.components_table
            selected_row = components_table.selectionModel().currentIndex().row() 
            remove_component_action = context_menu.addAction("Remove Component")
            remove_component_action.triggered.connect(lambda: self.remove_component(components_table, selected_row))
        else:
            return         
 
        # Get the global position of the cursor
        cursor_position = QCursor.pos()
        context_menu.exec_(cursor_position)

    
    def contextMenuEvent(self, event):
        self.create_context_menu(event.pos())