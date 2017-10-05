import time
import numpy as np
import ibmiotf.gateway
from sense_hat import SenseHat
import math


R = [255, 0, 0] # Red
W = [255, 255, 255]  # White
G = [0, 255, 0]  # Green
B = [0, 0, 0] # Black
    
maskLeft = [[],[10],[10,18],[10,18,26],[10,18,26,34],[10,18,26,34,42],[10,18,26,34,42,50],[10,18,26,34,42,50,9],[10,18,26,34,42,50,9,17],[10,18,26,34,42,50,9,17,25]]
maskRight = [[],[14],[14,22],[14,22,30],[14,22,30,38],[14,22,30,38,46],[14,22,30,38,46,54],[14,22,30,38,46,54,13],[14,22,30,38,46,54,13,21],[14,22,30,38,46,54,13,21,29]]


sense = SenseHat()
def getPixelMap(color, number): #not working for negative numbers
    redPlane = np.tile(R,64)
    redPlane.shape = (64,3)

    greenPlane = np.tile(G,64)
    greenPlane.shape = (64,3)

    blackPlane = np.tile(B, 64)
    blackPlane.shape = (64, 3)
    
    if color == "red":
        plane = redPlane
    elif color == "green":
        plane = greenPlane
    elif color == "black":
        plane = blackPlane;
        print('color is black');

    number = math.floor(number)
    if number >= 10:
        leftDigit = int(str(number)[0])
        rightDigit = int(str(number)[1])
        
        plane[maskLeft[leftDigit]] = W
        plane[maskRight[rightDigit]] = W
    
    elif number <=9:
        plane[maskRight[int(number)]] = W

    plane.shape = (64,3)
    return plane.tolist()


client = None

def myCommandCallback(cmd):
    if cmd.command == "display":
        command = cmd.data['screen']
        if command == "on":
            # TODO insert your code here
            sense.set_pixels(getPixelMap("red", sense.get_temperature()));
        elif command == "off":
            # TODO insert your code here
            sense.set_pixels(getPixelMap("green", sense.get_temperature()));

try:
    last_temp = sense.get_temperature(); # initialise
    THRESHOLD_TEMP = 29;
    first_message = False;
    bgColor = "black";
    gatewayOptions = {"org": "0sq3bo", "type": "raspberryGW", "id": "b827eb99a685", "auth-method": "token", "auth-token": "*V7yigNRFQ0ElL?!AM"}
    gatewayCli = ibmiotf.gateway.Client(gatewayOptions)

    gatewayCli.connect()
    gatewayCli.deviceCommandCallback = myCommandCallback 
    gatewayCli.subscribeToDeviceCommands(deviceType='senseHat', deviceId='senb827ebccf3d0', command='display',format='json',qos=2)

    while True:
        temp = sense.get_temperature(); # TODO insert your code here
        print('read temp ',temp);
        # Figure out whether bluemix has sent us a message yet
        if ((last_temp < THRESHOLD_TEMP and temp >= THRESHOLD_TEMP) or
			(last_temp >= THRESHOLD_TEMP and temp < THRESHOLD_TEMP) or first_message):
            print('inside big clause');
            first_message = True; # Bluemix has sent a message if we've crossed the threshold in either direction now or at any point in the past
            if (temp < THRESHOLD_TEMP):
                bgColor = "green";
            else:
                bgColor = "red";
        else: # Not initialised so use a black background
            bgColor = "black";
        print('about to set pixels for temp ',temp,' bgcolor ',bgColor);
        sense.set_pixels(getPixelMap(bgColor, temp));
        myData = {"d" : { "temperature" : temp }}; # TODO insert your code here
        gatewayCli.publishDeviceEvent("senseHat", "senb827ebccf3d0", "tempEvent", "json", myData, qos=1 )
        time.sleep(2)

except ibmiotf.ConnectionException  as e:
    print(e)
