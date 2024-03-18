import tkinter as tk

class AddAnimal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Add an Animal", font=controller.main_font)
        self.label.pack(side="top", fill="x", pady=10)

        debug_button = tk.Button(self, text="Go Back", font=controller.main_font, command=lambda: controller.show_frame("Overview"))
        debug_button.place(relx=1.0, rely=0.0, anchor="ne")