import tkinter as tk
import subprocess
import os

# scans available wifi networks and returns a list of their names
def scan_wifi():
    networks = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])
    networks = networks.decode("utf-8") # converts the bytes to a string
    networks = networks.split("\n")     # splits the string into a list
    wifi_list = []

    for line in networks:
        if "ESSID" in line:
            wifi_list.append(line.split('"')[1])

    return wifi_list

def update_networks():
    ssid_menu["menu"].delete(0, "end")
    for ssid in scan_wifi():
        ssid_menu["menu"].add_command(label=ssid, command=lambda ssid=ssid: ssid_var.set(ssid))

def connect_to_wifi(ssid, password):
    os.system('sudo raspi-config nonint do_wifi_ssid_passphrase ' + ssid + " " + password)
    print(f"Verbindung zu {ssid} mit Passwort {password} wird hergestellt...")

window = tk.Tk()
window.title("WLAN-Verbindung")

tk.Label(text="Wählen Sie ein WLAN-Netzwerk:", font=("Arial", 12), height=2, width=10).pack()

# Dropdown with available networks
ssid_var = tk.StringVar()
ssid_menu = tk.OptionMenu(window, ssid_var, *scan_wifi())
ssid_menu.pack()

# button to update the list of available networks
update_button = tk.Button(text="Netzwerke aktualisieren", command=update_networks)
update_button.pack()

# password input
password_var = tk.StringVar()
tk.Label(text="Passwort:", font=("Arial", 12)).pack()
password_entry = tk.Entry(window, textvariable=password_var, show="*")
password_entry.pack()

# button to connect to the selected network
connect_button = tk.Button(text="Verbinden", command=lambda: connect_to_wifi(ssid_var.get(), password_var.get()))
connect_button.pack()

# start the window
window.mainloop()
