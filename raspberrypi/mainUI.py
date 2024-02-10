import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import *
import subprocess
import requests
import os

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.after(4000, self.attributes, '-fullscreen', True)
        
        self.main_font = tkfont.Font(family='Helvetica', size=14, weight="normal")

        # Container for stacking frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary of frames
        self.frames = {}
        for F in (WelcomePage, WifiSetup, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Virtual keyboard setup (initially hidden)
        self.keyboard_shift = False
        self.keyboard_frame = tk.Frame(self, bg="lightgray")
        self.keyboard_frame.pack(side="bottom", fill="x")
        self.create_keyboard()

        # Show welcome page
        self.show_frame("WelcomePage")
        self.hide_keyboard()

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def create_keyboard(self):
        """Creates the virtual keyboard layout"""
        keyboard_buttons = [
            ["!", '"', "#", "$", "%", "&", "/", "(", ")", "?"],
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["q", "w", "e", "r", "t", "z", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", "Hide"],
            ["Shift", "y", "x", "c", "Space", "v", "b", "n", "m", "DEL"]
            
        ]


        for row, key_list in enumerate(keyboard_buttons):
            for col, key in enumerate(key_list):
                if key == "Shift":
                    button = tk.Button(self.keyboard_frame, text=key, font=self.main_font,
                                       command=lambda key=key: self.handle_keyboard_input(key),
                                       width=3, height=1, bg="lightgray")
                elif key == "DEL":
                    button = tk.Button(self.keyboard_frame, text=key, font=self.main_font,
                                       command=lambda key=key: self.handle_keyboard_input(key),
                                       width=3, height=1, bg="lightgray")
                elif key == "Hide":
                    button = tk.Button(self.keyboard_frame, text=key, font=self.main_font,
                                       command=lambda key=key: self.handle_keyboard_input(key),
                                       width=3, height=1, bg="lightgray")
                elif key == "Space":
                    button = tk.Button(self.keyboard_frame, text=key, font=self.main_font,
                                        command=lambda key=key: self.handle_keyboard_input(key),
                                        width=6, height=1, bg="white")
                else:
                    button = tk.Button(self.keyboard_frame, text=key, font=self.main_font,
                                    command=lambda key=key: self.handle_keyboard_input(key),
                                    width=3, height=1, bg="white")
                button.grid(row=row, column=col, padx=2, pady=2)

    def show_keyboard(self):
        """Shows the virtual keyboard"""
        self.keyboard_frame.pack(side="bottom", fill="x")
    
    def hide_keyboard(self):
        """Hides the virtual keyboard"""
        self.keyboard_frame.pack_forget()

    def handle_keyboard_input(self, key):
        """Handles input from the virtual keyboard"""

        #char map for special characters which get swapped on shift
        special_chars = {
            "!": "*",
            '"': "-",
            "#": "_",
            "$": "+",
            "%": "=",
            "&": "<",
            "/": ">",
            "(": "@",
            ")": "^",
            "?": "`",
        }
        
        active_entry = self.focus_get()
        if active_entry:
            if key == "DEL":
                active_entry.delete(len(active_entry.get())-1, tk.END)
            elif key == "Hide":
                self.hide_keyboard()
            elif key == "Shift":
                self.switch_keyboard_on_shift()
                self.keyboard_shift = not self.keyboard_shift
            elif key == "Space":
                active_entry.insert(tk.END, " ")
            else:
                if self.keyboard_shift:
                    if key in special_chars:
                        key = special_chars[key]
                    else:
                        key = key.upper()
                active_entry.insert(tk.END, key)
    
    def switch_keyboard_on_shift(self):
        """Switches the case of the virtual keyboard buttons"""
        #char map for special characters
        specialchar_map = {
            "!": "*",
            '"': "-",
            "#": "_",
            "$": "+",
            "%": "=",
            "&": "<",
            "/": ">",
            "(": "@",
            ")": "^",
            "?": "`",
            "*": "!",
            "-": '"',
            "_": "#",
            "+": "$",
            "=": "%",
            "<": "&",
            ">": "/",
            "@": "(",
            "^": ")",
            "`": "?"
        }

        
        # Get all buttons from the keyboard frame
        buttons = self.keyboard_frame.winfo_children()

        # Iterate through each button
        for button in buttons:
            # Convert existing text to a list of characters
            chars = list(button['text'])

            # exclude special buttons
            if button['text'] in ["Shift", "DEL", "Hide", "Space"]:
                continue

            # Toggle the case of each character
            chars = [specialchar_map.get(char, char.upper() if char.islower() else char.lower()) if char.isalpha() else specialchar_map.get(char, char) for char in chars]
                
            # Rebuild the text and update the button label
            button['text'] = ''.join(chars)            
    


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

        available_networks = self.scan_wifi()

        can = Canvas(self, height=480, width=800)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)

        label = tk.Label(can, text="Wählen Sie ein WLAN-Netzwerk:", font=controller.main_font, height=2, width=35)
        label.pack(side="top", fill="x", pady=10)

        # create canvas with scrollbar and listbox for the available networks
        listCanavas = Canvas(can)
        listCanavas.pack()

        # create scrollbar
        scrollbar = Scrollbar(listCanavas, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)

        # create listbox for the available networks
        self.network_list = Listbox(listCanavas, font=("Arial", 12))
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
        update_button = tk.Button(can, text="Netzwerke aktualisieren", image=refreshImage, command=self.update_networks)
        update_button.pack()

        # password input
        self.password_var = tk.StringVar()
        tk.Label(can, text="Passwort:", font=("Arial", 12), height=2, width=35).pack()
        password_entry = tk.Entry(can, textvariable=self.password_var, show="*")
        password_entry.pack()
        password_entry.bind("<FocusIn>", lambda event: controller.show_keyboard())
        password_entry.bind("<FocusOut>", lambda event: controller.hide_keyboard())

        # button to connect to the selected network
        connect_button = tk.Button(can, text="Verbinden", command=lambda: self.connect_to_wifi(get_selected_network(), self.password_var.get()), pady=10, background="grey", foreground="white", font=controller.main_font)
        connect_button.pack()

        close_window_button = tk.Button(can, text="Close", command=lambda: controller.destroy(), pady=10, background="grey", foreground="white", font=controller.main_font)
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
        self.network_list.delete(0, END)        
        for ssid in self.scan_wifi():
            self.network_list.insert(END, ssid)

    def connect_to_wifi(self, ssid, password):
        if not ssid:
            print("Please select a network")
            return
        #try 3 times to connect to the network
        for i in range(3):
            os.system('sudo raspi-config nonint do_wifi_ssid_passphrase "' + ssid + '" ' + password )
            print(f"Verbindung zu {ssid} mit Passwort {password} wird hergestellt...")
            if self.hasInternet():
                print("Connected to the network")
                self.controller.show_frame("PageTwo")
            else:
                print("Failed to connect to the network")
    
    def hasInternet(self):
        # Check if the device has internet
        try:
            requests.get("https://www.google.com")
            return True
        except:
            return False


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="YALLAH", font=controller.main_font, height=2, width=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        close_window_button = tk.Button(self, text="Close", command=lambda: controller.destroy(), pady=10, background="grey", foreground="white", font=controller.main_font)
        close_window_button.pack()
        

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
