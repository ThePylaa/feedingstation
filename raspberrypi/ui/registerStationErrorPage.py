import tkinter as tk

class RegisterStationErrorPage(tk.Frame):
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Failed to register the station", font=controller.main_font, height=2, width=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Try again", command=lambda: controller.show_frame("RegisterStation"))
        button.pack()   

