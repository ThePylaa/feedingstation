from tkinter import Tk
import time
from arduinoCommunication import dispensePortion


class ManualFeeding(Tk.frame):
    def __init__(self, parent, controller):
        Tk.frame.__init__(self, parent)
        self.controller = controller

        
        self.label = Tk.Label(self, text="Dispensing Portion...", font=controller.main_font)
        #center label
        self.label.pack(side="top", fill="x", pady=10)
        #dispense portion
        dispensePortion(1)
        #wait for 3 seconds
        time.sleep(3)
        #show the overview page
        controller.show_frame("Overview")
        return
        
