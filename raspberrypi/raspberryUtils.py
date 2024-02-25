from arduinoCommunication import *
from rtc import *
import time 
import io
import requests
import json
from datetime import datetime
from picamera2 import Picamera2

# Load the environment variables
with open("/home/pi/Desktop/feedingstation/raspberrypi/config.json", "r") as file:
    config = json.loads(file.read())
api_host= config["API_HOST"]
station_uuid = config["DEVICE_UUID"]
user_id = config["USER_ID"]
global dispensedPortions
global lastScheduleRefresh

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

def sendImage():
    picam2 = Picamera2()
    picam2.configure(picam2.create_capture_configuration())
    picam2.start()
    time.sleep(1)
    data = io.BytesIO()
    picam2.capture_file(data, format='jpeg')

    try:
        res = requests.post(f"{api_host}/picture/upload_picture", json={"user_id":  user_id, "feedingstation_id": station_uuid, "picture": data.getvalue(), "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    except Exception as e:
        print(e)
        print("Failed to upload picture to server")


def getSchedule():
    # Get the schedule from the server and saves it to the schedule.json file
    try:
        res = requests.get(f"{api_host}/portion/portions?feedingstation={station_uuid}")
        schedule = res.json()
        print(schedule)
        with open("/home/pi/Desktop/feedingstation/raspberrypi/schedule.json", "w") as file:
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
    
def doRoutine(lastServerUpdate):
    print("Doing Main Routine")

    #the server will be updated every 5 minutes but the schedule will be checked every 10 seconds
    if getTimeInSeconds() - lastServerUpdate > 300:
        
        if hasInternet():
            print("Updating server and getting schedule")
            updateServer()
            getSchedule()
            #Also updating the RTC
            setRtcTime()
        
        lastServerUpdate = getTimeInSeconds()
    
    # every 24 hours all portions will be set to not dispensed, timewindow of 5 minutes
    if (datetime.datetime.now() - lastScheduleRefresh).days >= 1:
        dispensedPortions = []
        lastScheduleRefresh = datetime.datetime.now()

    # Check if rfid is present
    rfid = getRFID()

    # If rfid is present, check if the rfid is in the schedule
    if rfid:
        with open("/home/pi/Desktop/feedingstation/raspberrypi/schedule.json", "r") as file:
            schedule = json.loads(file.read())
            for animal in schedule:
                if animal["animal_rfid"] == rfid:
                    print("RFID found in schedule")
                    # Check if weight is present, if bigger than 5, dont dispense food
                    if getFoodbowlWeight() > 5:
                        print("Foodbowl is not empty")
                        #TODO Mabye insert notification to the user
                        break
                    # If the rfid is in the schedule, dispense a portion of food if the time of the last portion["time"] is smaller than the current time
                    for portion in animal["portions"]:
                        if getRtcDateTime().time() > datetime.strptime(portion["time"], "%H:%M:%S").time() and portion["time"] not in dispensedPortions:
                            print(f"Dispensing %s portions of food" % portion["size"])                               
                            dispensePortion(portion["size"])
                            #TODO, sleep has to be adjusted to the time it takes to dispense the food
                            time.sleep(1)
                            sendImage()
                            # tags portion as dispensed
                            dispensedPortions.append(portion["time"])

                            with open("/home/pi/Desktop/feedingstation/raspberrypi/schedule.json", "w") as file:
                                file.write(json.dumps(schedule))
                                break    
        
    return lastServerUpdate

if __name__ == "__main__":
    # Main loop
    lastServerUpdate = getTimeInSeconds() - 300

    while True:
        lastServerUpdate = doRoutine(lastServerUpdate)
        time.sleep(2)
