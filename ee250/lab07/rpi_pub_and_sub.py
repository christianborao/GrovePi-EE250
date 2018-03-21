"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time

import sys
sys.path.append('../../Software/Python/')

from grovepi import *

led = 2
button = 3
ultrasonic_ranger = 4

pinMode(led, "OUTPUT")
pinMode(button, "INPUT")


#my custom callback

def led_callback(client, data, msg):

    data = str(msg.payload, "utf-8")
    
    if (data == "LED_ON"):
        print("Test")
        digitalWrite(led,1)
    elif (data == "LED_OFF"):
        digitalWrite(led, 0)


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("anrg-pi5/ultrasonicRanger")
    client.subscribe("anrg-pi5/led")
    client.subscribe("anrg-pi5/button")

    #add the custom callback:

    client.message_callback_add("anrg-pi5/led", led_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        
        # loop and read the ultrasonic ranger in 1 second intervals
        # and publish the distance values to anrg-pi5/ultrasonicRanger
        time.sleep(1)

        #read ultrasonic data:
        data = str(ultrasonicRead(ultrasonic_ranger))

        #publish the ultrasonic data
        client.publish("anrg-pi5/ultrasonicRanger", data)

        #monitor the button:
        button_status = digitalRead(button)

        if (button_status)
            client.publish("anrg-pi5/button", "Button pressed!")




