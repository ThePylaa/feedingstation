import tkinter as tk
import requests
import json

class RegisterStation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Register Station", font=controller.main_font)
        self.label.pack(side="top", fill="x", pady=10)

        self.station_name_label = tk.Label(self, text="Station Name", font=controller.main_font)
        self.station_name_label.pack()
        self.station_name_entry = tk.Entry(self, font=controller.main_font)
        self.station_name_entry.pack()

        self.email_label = tk.Label(self, text="Email", font=controller.main_font)
        self.email_label.pack()
        self.email_entry = tk.Entry(self, font=controller.main_font)
        self.email_entry.pack()

        self.password_label = tk.Label(self, text="Password", font=controller.main_font)
        self.password_label.pack()
        self.password_entry = tk.Entry(self, font=controller.main_font, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(self, text="Register", font=controller.main_font, command=lambda: self.register_station())
        self.register_button.pack()

    def register_station(self):
        print("Registering station")
        station_name = self.station_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        with open("./raspberrypi/config.json", "r") as file:
            config = json.loads(file.read())
        api_host= config["API_HOST"]

        try:
            loginRes = requests.post(f"{api_host}/user/login?email={email}&password={password}")
            loginRes = loginRes.json()
            user_id = loginRes["user_id"]

            station_id = requests.get(f"{api_host}/feedingstation/new_station_uuid")
            station_id = station_id.json()

            registerRes = requests.post(f"{api_host}/feedingstation/register", json={"feedingstation_id": station_id, "user_id": user_id, "name": station_name})

            if registerRes.status_code == 200:
                config["STATION_ID"] = station_id
                config["STATION_NAME"] = station_name
                with open("./raspberrypi/config.json", "w") as file:
                    file.write(json.dumps(config))

                self.controller.show_frame("RegisterStationSuccess")
            else:
                self.controller.show_frame("RegisterStationErrorPage")
        except:
            self.controller.show_frame("RegisterStationErrorPage")
