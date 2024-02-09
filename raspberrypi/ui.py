import tkinter as tk
from tkinter import messagebox
import subprocess

def check_credentials():
    user = username_entry.get()
    password = password_entry.get()
    # Hier können Sie die Anmeldeinformationen überprüfen
    if user == "admin" and password == "admin":
        messagebox.showinfo("Erfolg", "Anmeldung erfolgreich!")
    else:
        messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort")


root = tk.Tk()
root.title("Anmeldefenster")

username_label = tk.Label(root, text="Benutzername")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Passwort")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

submit_button = tk.Button(root, text="Anmelden", command=check_credentials)
submit_button.pack()


root.mainloop()
