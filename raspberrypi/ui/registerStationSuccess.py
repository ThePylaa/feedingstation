import tkinter as tk

class RegisterStationSuccess(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Station registered successfully", font=controller.main_font, height=2, width=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Close", command=lambda: controller.destroy(), pady=10, background="grey", foreground="white", font=controller.main_font)
        button.pack()