import numpy as np
from Sinusoid import Sinusoid
class ComposedSignal:
    composed_signals_list=[] 
    selected_index= 0
    def __init__(self):
        self.component_list_numpy=[]
        self.component_list_sinusoid=[]
        self.t_window= None
        self.composed_signal=None

    def compose_signal(self):
        self.composed_signal= np.sum(self.component_list_numpy, axis=0)
    
    def add_component(self, freq, amp, phase, attr_list= None):
        sinusoid= Sinusoid(freq, amp, phase)
        self.component_list_sinusoid.append(sinusoid)
        if attr_list is not None:
            attr_list.addItem(f"Component: amplitude= {amp}, freq= {freq}, phase= {phase}")
    
    @classmethod
    def remove_component(cls,component_list_widget, index):
        selected_signal= cls.composed_signals_list[cls.selected_index]
        _=selected_signal.component_list_numpy.pop(index)
        _=selected_signal.component_list_sinusoid.pop(index)
        selected_signal.compose_signal()
        component_list_widget.takeItem(index)
   
    @classmethod
    def show_components(cls, component_list_widget, index): #index used to know which signal to show its components 
        component_list_widget.clear()
        selected_signal= cls.composed_signals_list[index]
        cls.selected_index=index
        component_list_widget.clear()
        component_num=1
        for comp in selected_signal.component_list_sinusoid:
            component_list_widget.addItem(f"Component {component_num}: amplitude= {comp.amp}, frequency= {comp.freq}, phase= {comp.phase}")
            component_num+=1
    
    def save_signal(self, signals_List):
        max_freq=self.get_max_freq()
        print(f"max_freq{max_freq}")
        end_window= int(1000/(2*max_freq))
        points_in_time= 3000
        self.t_window= np.linspace(0,end_window,points_in_time)
        self.component_list_numpy = [sinusoid.generate_sinusoid(self.t_window) for sinusoid in self.component_list_sinusoid]
        self.compose_signal()
        ComposedSignal.composed_signals_list.append(self)
        signals_List.addItem(f"Composed Signal {len(ComposedSignal.composed_signals_list)}")
   
    @classmethod
    def remove_signal(cls,signals_List_widget, components_list, index):
        removed_signal= cls.composed_signals_list.pop(index) #remove composedSignal instance and return it
        del removed_signal.component_list_numpy
        del removed_signal.component_list_sinusoid
        signals_List_widget.takeItem(index)
        components_list.clear()

    def get_composed_signal(self):
        return self.composed_signal

    def get_max_freq(self):
        frequencies_list=[]
        for sinusoid in self.component_list_sinusoid:
            frequencies_list.append(sinusoid.freq)
        max_freq= max(frequencies_list)
        return max_freq
    
    def to_csv(self):
         file_name= f"output{len(ComposedSignal.composed_signals_list)}.csv"
         data= np.column_stack((self.t_window, self.composed_signal))
         np.savetxt(file_name, data, delimiter=",", comments='', fmt='%f')
         return file_name


def set_default_composer(signals_list):
    composed1= ComposedSignal()
    composed2= ComposedSignal()
    composed3= ComposedSignal()

    composed1.add_component(freq=5, amp=2, phase=0)
    composed1.add_component(freq=4, amp=3, phase=0)
    composed1.add_component(freq=3, amp=1, phase=0)
    composed1.save_signal(signals_list)

    composed2.add_component(freq=1, amp=1, phase=0)
    # composed2.add_component(freq=2, amp=1, phase=90)
    # composed2.add_component(freq=3, amp=1, phase=90)
    composed2.save_signal(signals_list)

    composed3.add_component(freq=28, amp=1, phase=0)
    composed3.add_component(freq=2, amp=1, phase=0)
    composed3.add_component(freq=3, amp=1, phase=0)
    composed3.save_signal(signals_list)




