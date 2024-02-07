import serial
import time
import random
import json

# Open serial connection to arduino
ser = serial.Serial('/dev/ttyACM0', 9600)
# Wait for connection to be established
time.sleep(1)


def dispensePortion():
    # Dispense 1 portion of food
    ser.write(b'1')

def getFoodbowlWeight():
    payload = recievePayload()
    return payload["weight"]
    
def isBarrierBroke():
    payload = recievePayload()
    return payload["broken"]
    
def getHumidity():
    payload = recievePayload()
    return payload["humidity"]
   
def getTemperature():
    payload = recievePayload()
    return payload["temp"]
    
def recievePayload():
    msg = ser.readline().decode("utf-8").strip()
    while(not msg.startswith("{") or not msg.endswith("}")):
        time.sleep(random.randint(0, 4) / 10)
        msg = ser.readline().decode("utf-8").strip()

    #RFID has to be converted to decimal
    jsonPayload = json.loads(msg)
    
    #checks if rfid is present
    if jsonPayload["rfid"] == "----NORFID----":
        return jsonPayload
    
    #splits raw["rfid"] into a list of strings and converts them from hex to decimal
    #first 10 characters are the RFID id
    #last 4 characters are the country code
    rfidID = int(jsonPayload["rfid"][:10], 16)
    rfidCountryCode = int(jsonPayload["rfid"][10:], 16)

    jsonPayload["rfid"] = str(rfidCountryCode)+str(rfidID)

    return jsonPayload
