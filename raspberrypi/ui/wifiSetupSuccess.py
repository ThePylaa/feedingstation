import tkinter as tk

class WifiSetupSuccess(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Network connection established", font=controller.main_font, height=2, width=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Register Station", command=lambda: controller.show_frame("RegisterStation"))
        button.pack()

        close_window_button = tk.Button(self, text="Close", command=lambda: controller.destroy(), pady=10, background="grey", foreground="white", font=controller.main_font)
        close_window_button.pack()