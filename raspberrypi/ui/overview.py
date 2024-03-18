import tkinter as tk

class Overview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Overview", font=controller.main_font)
        self.label.pack(side="top", fill="x", pady=10)

        self.addAnimal_button = tk.Button(self, text="Add Animal", font=controller.main_font, command=lambda: controller.show_frame("AddAnimal"))
        self.addAnimal_button.pack()

        self.manualFeeding_button = tk.Button(self, text="Dispense 1 Portion", font=controller.main_font, command=lambda: controller.show_frame("ManualFeeding"))

        debug_button = tk.Button(self, text="Close", command=lambda: controller.destroy(), pady=10, font=controller.main_font)
        debug_button.place(relx=1.0, rely=0.0, anchor="ne")
