from arduinoCommunication import isBarrierBroke, getTemperature, getHumidity, getFoodbowlWeight, dispensePortion
import time 
from dotenv import load_dotenv
import os
import requests
import json


# Load the environment variables
load_dotenv()
api_host= os.getenv("API_HOST")
station_uuid = os.getenv("DEVICE_UUID")    

def updateServer():
    # Update the server with the current status of the feeding stations humidity and temperature
    try:
        hum = getHumidity()
        broken = isBarrierBroke()

        res = requests.put(f"{api_host}/feedingstation/update_humidity", json={"feedingstation_id": station_uuid, "humidity": hum})
        res = requests.put(f"{api_host}/feedingstation/update_container_foodlevel", json={"feedingstation_id": station_uuid, "container_foodlevel": broken})
    
    except Exception as e:
        print(e)
        print("Failed to update server")

def getSchedule():
    # Get the schedule from the server and saves it to the schedule.json file
    try:
        res = requests.get(f"{api_host}/portion/portions?feedingstation={station_uuid}")
        schedule = res.json()
        print(schedule)
        with open("schedule.json", "w") as file:
            file.write(json.dumps(schedule))
    except Exception as e:
        print(e)
        print("Failed to get schedule from server")

def hasInternet():
    # Check if the device has internet
    try:
        requests.get("https://www.google.com")
        return True
    except:
        return False

if __name__ == "__main__":
    # Main loop
    # Two different modes, one for when the device has internet and one for when it doesn't
    exit()
    while True:
        if hasInternet():
            # If the device has internet, it will update the server with the current status of the feeding station
            # and get the schedule from the server
            updateServer()
            getSchedule()
            time.sleep(5)
            try:
                with open("schedule.json", "r") as file:
                    schedule = json.loads(file.read())
                    print(schedule)
                    for portion in schedule:
                        if time.time() > portion["time"]:
                            dispensePortion(portion["amount"])
                            schedule.remove(portion)
                            with open("schedule.json", "w") as file:
                                file.write(json.dumps(schedule))
            except Exception as e:
                print(e)
                print("Failed to dispense food")
        else:
            # If the device doesn't have internet, it will use the schedule.json file to dispense food
            try:
                with open("schedule.json", "r") as file:
                    schedule = json.loads(file.read())
                    print(schedule)
                    for portion in schedule:
                        if time.time() > portion["time"]:
                            dispensePortion(portion["amount"])
                            schedule.remove(portion)
                            with open("schedule.json", "w") as file:
                                file.write(json.dumps(schedule))
            except Exception as e:
                print(e)
                print("Failed to dispense food")
            time.sleep(5)

