import tkinter as tk
from tkinter import *

class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        can = Canvas(self, height=150)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)

        label = tk.Label(can, text="Hello! This is the setup for your feedingstation.\nYou need Wifi to complete this Setup.\nTo get started, press the buttom below!", font=controller.main_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Button(can, text="Get Started!", command=lambda: controller.show_frame("WifiSetup"), pady=10, background="grey", foreground="white", font=controller.main_font).pack()
