import serial
import time
# Open serial connection to arduino
ser = serial.Serial('/dev/ttyACM0', 9600)
# Wait for connection to be established
time.sleep(1)


def dispensePortion():
    # Dispense 1 portion of food
    ser.write(b'1')

def getFoodbowlWeight():
    # Request the weight of the food bowl
    ser.write(b'2')
    # Read the response from the arduino
    msg = ser.readline().decode("utf-8").strip()
    # Return the weight
    return msg

def isBarrierBroke():
    # Request the status of the barrier
    ser.write(b'3')
    # Read the response from the arduino
    msg = ser.readline().decode("utf-8").strip()
    # Return the status
    if msg == "1":
        return True
    else:
        return False

def getHumidity():
    # Request the humidity from the arduino
    ser.write(b'4')
    # Read the response from the arduino
    msg = ser.readline().decode("utf-8").strip()
    # Return the humidity
    return msg

def getTemperature():
    # Request the temperature from the arduino
    ser.write(b'5')
    # Read the response from the arduino
    msg = ser.readline().decode("utf-8").strip()
    # Return the temperature
    return msg