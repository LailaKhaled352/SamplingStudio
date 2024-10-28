import numpy as np
from Sinusoid import Sinusoid
class ComposedSignal:
    composed_signals_list=[] 
    selected_index= 0
    def __init__(self):
        self.component_list_numpy=[]
        self.component_list_sinusoid=[]
        self.t_window= np.linspace(0,20,1000)
        self.composed_signal=None

    def compose_signal(self):
        self.composed_signal= np.sum(self.component_list_numpy, axis=0)
    
    def add_component(self, freq, amp, phase, attr_list):
        sinusoid= Sinusoid(freq, amp, phase)
        self.component_list_sinusoid.append(sinusoid)

        sinusoid_generated= sinusoid.generate_sinusoid(self.t_window)
        self.component_list_numpy.append(sinusoid_generated)

        self.compose_signal()
        attr_list.addItem(f"Component_n: amplitude= {amp}, freq= {freq}, phase= {phase}")
    @classmethod
    def remove_component(cls,component_list_widget, index):
        selected_signal= cls.composed_signals_list[cls.selected_index]
        _=selected_signal.component_list_numpy.pop(index)
        _=selected_signal.component_list_sinusoid.pop(index)
        selected_signal.compose_signal()
        component_list_widget.takeItem(index)
   
    @classmethod
    def show_components(cls, component_list_widget, index): #index used to know which signal to show its components 
        selected_signal= cls.composed_signals_list[index]
        cls.selected_index=index
        for comp in selected_signal.component_list_sinusoid:
            component_list_widget.addItem(f"Component_n: amplitude= {comp.amp}, frequency= {comp.freq}, phase= {comp.phase}")
    
    def save_signal(self, signals_List):
        ComposedSignal.composed_signals_list.append(self)
        print(len(self.component_list_sinusoid))
        print(len(ComposedSignal.composed_signals_list))
        signals_List.addItem(f"Composed_signal {len(ComposedSignal.composed_signals_list)}")
   
    @classmethod
    def remove_signal(cls,signals_List_widget, index):
        _= cls.composed_signals_list.pop(index) #remove composedSignal object
        signals_List_widget.takeItem(index)

    def get_composed_signal(self):
        return self.composed_signal

    def load_composed_signal(self):
        signal_data_time, signal_data_amplitude= self.t_window, self.composed_signal
        return  signal_data_time, signal_data_amplitude

    def get_max_freq(self):
        frequencies_list=[]
        for sinusoid in self.component_list_sinusoid:
            frequencies_list.append(sinusoid.freq)
        max_freq= max(frequencies_list)
        return max_freq