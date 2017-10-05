import time
import numpy as np
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import math
import json


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
def on_connect(client,userdata,flags,rc):
    print("Connected with result code"+str(rc));
    print(client.subscribe("iot-2/cmd/display/fmt/json"));
#    topic = "iot-2/type/senseHat/id/senb827ebccf3d0/evt/tempEvent/fmt/json";
#    client.loop_start();
#    while client.loop() == 0:
#        msg = json.JSONEncoder().encode({"d":{"temperature":sense.get_temperature()}});
#        client.publish(topic, payload=msg, qos=2, retain=False);
#        print("published ",msg);
#        time.sleep(5);
#    print("exiting while");

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "display":
        command = msg.userdata['screen']
        if command == "on":
            sense.set_pixels(getPixelMap("red", sense.get_temperature()));
        elif command == "off":
            # TODO insert your code here
            sense.set_pixels(getPixelMap("green", sense.get_temperature()));

def on_disconnect(client, userdata, rc):
	print("Disconnected with result code"+str(rc));

clientId = "g:0sq3bo:raspberryGW:b827eb99a685";
#clientId = "d:0sq3bo:senseHat:senb827ebccf3d0";
broker = "0sq3bo.messaging.internetofthings.ibmcloud.com";
mqttc = mqtt.Client(clientId);
mqttc.username_pw_set("use-token-auth",password="*V7yigNRFQ0ElL?!AM");
#mqttc.username_pw_set("use-token-auth","dn3ZGIz?L5QDU_(NWg");

mqttc.on_connect = on_connect;
mqttc.on_message = on_message;
mqttc.on_disconnect = on_disconnect;
mqttc.connect(host=broker, port=1883, keepalive=60);
#mqttc.subscribe("iot-2/cmd/display/fmt/json");
#mqttc.subscribe("iot-2/cmd/+/fmt/json");
#mqttc.loop_start();
#topic = "iot-2/evt/tempEvent/fmt/json";
#topic = "iot-2/type/senseHat/id/senb827ebccf3d0/evt/tempEvent/fmt/json";
#while mqttc.loop() == 0:
#    msg = json.JSONEncoder().encode({"d":{"temperature":sense.get_temperature()}});
#    mqttc.publish(topic, payload=msg, qos=2, retain=False);
#    print("published ",msg);
#    time.sleep(2);
#    pass;
mqttc.loop_forever();
