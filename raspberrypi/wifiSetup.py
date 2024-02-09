import os
import subprocess


def scan_wifi():
    networks = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])
    networks = networks.decode("utf-8") # Konvertiert die Bytes in einen String
    networks = networks.split("\n")     # Splittet den String in eine Liste
    wifi_list = []

    for line in networks:
        if "ESSID" in line:
            wifi_list.append(line.split('"')[1])

    return wifi_list


wifi_list = scan_wifi()

for i, wifi in enumerate(wifi_list):
    print(f"{i+1}. {wifi}")

choice = int(input("Wählen Sie ein WiFi-Netzwerk aus (geben Sie die entsprechende Nummer ein): "))
print(f"Sie haben {wifi_list[choice-1]} ausgewählt.")
password = input("Geben Sie das Passwort für das WiFi-Netzwerk ein: ")
print(f"Das Passwort {password} wurde eingegeben.")


os.system('sudo raspi-config nonint do_wifi_ssid_passphrase ' + wifi_list[choice-1] + " " + password)