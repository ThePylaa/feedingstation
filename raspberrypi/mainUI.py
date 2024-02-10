import tkinter as tk                
from tkinter import font as tkfont  
from tkinter import *
import subprocess
import os

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.main_font = tkfont.Font(family='Helvetica', size=14, weight="normal")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        

        self.frames = {}
        for F in (WelcomePage, WifiSetup, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        can = Canvas(self, height=150)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)

        label = tk.Label(can, text="Hello! This is the setup for your feedingstation.\nYou need Wifi to complete this Setup.\nTo get started, press the buttom below!", font=controller.main_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Button(can, text="Get Started!", command=lambda: controller.show_frame("WifiSetup"), pady=10, background="grey", foreground="white", font=controller.main_font).pack()


class WifiSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        can = Canvas(self, height=350, width=700)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)

        label = tk.Label(can, text="Wählen Sie ein WLAN-Netzwerk:", font=controller.main_font, height=2, width=35)
        label.pack(side="top", fill="x", pady=10)

        # Dropdown with available networks
        self.ssid_var = tk.StringVar()
        self.ssid_var.set("Netzwerk wählen")
        self.ssid_menu = tk.OptionMenu(can, self.ssid_var, *self.scan_wifi())
        self.ssid_menu.config(bg="blue", fg="white")
        self.ssid_menu.pack()

        # button to update the list of available networks
        update_button = tk.Button(can, text="Netzwerke aktualisieren", command=self.update_networks, pady=10, background="grey", foreground="white", font=controller.main_font)
        update_button.pack()

        # password input
        password_var = tk.StringVar()
        tk.Label(can, text="Passwort:", font=("Arial", 12), height=2, width=35).pack()
        password_entry = tk.Entry(can, textvariable=password_var, show="*")
        password_entry.pack()

        # button to connect to the selected network
        connect_button = tk.Button(can, text="Verbinden", command=lambda: self.connect_to_wifi(self.ssid_var.get(), password_var.get()), pady=10, background="grey", foreground="white", font=controller.main_font)
        connect_button.pack()

        close_window_button = tk.Button(can, text="Close", command=lambda: controller.destroy(), background="grey", foreground="white", font=controller.main_font)
        close_window_button.pack()

    def scan_wifi(self):
        networks = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])
        networks = networks.decode("utf-8") # converts the bytes to a string
        networks = networks.split("\n")     # splits the string into a list
        wifi_list = []

        for line in networks:
            if "ESSID" in line:
                wifi_list.append(line.split('"')[1])

        return wifi_list

    def update_networks(self):
        self.ssid_menu["menu"].delete(0, "end")
        for ssid in self.scan_wifi():
            self.ssid_menu["menu"].add_command(label=ssid, command=lambda ssid=ssid: self.ssid_var.set(ssid))

    def connect_to_wifi(ssid, password):
        os.system('sudo raspi-config nonint do_wifi_ssid_passphrase ' + ssid + " " + password)
        print(f"Verbindung zu {ssid} mit Passwort {password} wird hergestellt...")




class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="YALLAH", font=controller.main_font, height=2, width=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        

if __name__ == "__main__":
    app = MainApp()
    app.attributes("-fullscreen", True)
    app.mainloop()