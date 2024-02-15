import tkinter as tk
from tkinter import *
import subprocess
import os
from raspberryUtils import hasInternet


class WifiSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        available_networks = self.scan_wifi()

        can = Canvas(self, height=480, width=800)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)

        label = tk.Label(can, text="Chose your Wifi Network:", font=controller.main_font, height=2, width=35)
        label.pack(side="top", fill="x", pady=10)

        # create canvas with scrollbar and listbox for the available networks
        listCanavas = Canvas(can)
        listCanavas.pack()

        # create scrollbar
        scrollbar = Scrollbar(listCanavas, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)

        # create listbox for the available networks
        self.network_list = Listbox(listCanavas, font=("Arial", 12), height=5)
        self.network_list.pack(padx=10, pady=10)

        # attach listbox to scrollbar
        self.network_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.network_list.yview)

        # insert available networks into the listbox
        for networks in available_networks:
            self.network_list.insert(END, networks)

        # Function to get the selected network
        def get_selected_network():
            index = self.network_list.index(ACTIVE)
            if index != -1:  # Check if a selection exists
                return self.network_list.get(index)
            else:
                print("No network selected.")

        # button to update the list of available networks
        global refreshImage
        refreshImage = tk.PhotoImage(file="refresh.png")
        update_button = tk.Button(can, text="Refresh Networks", image=refreshImage, command=self.update_networks)
        update_button.pack()

        # password input
        self.password_var = tk.StringVar()
        tk.Label(can, text="Password:", font=("Arial", 12), height=2, width=35).pack()
        password_entry = tk.Entry(can, textvariable=self.password_var, show="*")
        password_entry.pack()
        password_entry.bind("<FocusIn>", lambda event: controller.show_keyboard())
        password_entry.bind("<FocusOut>", lambda event: controller.hide_keyboard())

        # button to connect to the selected network
        connect_button = tk.Button(can, text="Connect", command=lambda: self.connect_to_wifi(get_selected_network(), self.password_var.get()), pady=10, background="grey", foreground="white", font=controller.main_font)
        connect_button.pack()

        #debug button to show the next page, placed at the right top corner
        debug_button = tk.Button(self, text="Close", command=lambda: controller.destroy(), pady=10, background="grey", foreground="white", font=controller.main_font)
        debug_button.pack(side="right", anchor=NE)

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
        self.network_list.delete(0, END)     
        self.network_list.insert(END, "Scanning for networks...")
        self.update()

        new_networks = self.scan_wifi()
        self.network_list.delete(0, END)
        if not new_networks:
            self.network_list.insert(END, "No networks found")
        else:    
            for ssid in new_networks:
                self.network_list.insert(END, ssid)

    def connect_to_wifi(self, ssid, password):
        if not ssid:
            print("Please select a network")
            return
        #try 3 times to connect to the network
        for i in range(3):
            os.system('sudo raspi-config nonint do_wifi_ssid_passphrase "' + ssid + '" ' + password )
            print(f"Verbindung zu {ssid} mit Passwort {password} wird hergestellt...")
            if hasInternet():
                break
        if hasInternet():
            print("Connected to the network")
            self.controller.show_frame("WifiSetupSuccess")
            return
        else:
            print("Failed to connect to the network")
            self.controller.show_frame("WifiSetupErrorPage")
