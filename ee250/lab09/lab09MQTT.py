"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time


import sys
sys.path.append('../../Software/Python/')

from grovepi import *
from grove_rgb_lcd import *


#Note the grovepi seems to automatically know where the LCD is
#connected to, so I did not code the LCD port at all
#The same goes for the humidity/temperature sensor

led = 2
humidity_temperature = 4

#set LED port as an output
pinMode(led, "OUTPUT") 

class th02:
    
    ADDRESS = 0x40

    TH02_REG_STATUS = 0x00
    TH02_REG_DATA_H = 0x01
    TH02_REG_DATA_L = 0x02
    TH02_REG_CONFIG = 0x03
    TH02_REG_ID = 0x11

    TH02_STATUS_RDY_MASK = 0x01

    TH02_CMD_MEASURE_HUMI = [0x01]
    TH02_CMD_MEASURE_TEMP = [0x11]

    SUCCESS = 0

#my custom callback for the LCD
def lcd_callback(client, lcd_data, lcd_msg):

    #convert the incoming data so it can be sent to the LCD
    lcd_data = str(lcd_msg.payload, "utf-8")

    #I believe this initializes the LCD; the examples were unclear
    setRGB(0, 255, 0)
    
    #this sends the data received to the LCD
    setText(lcd_data)

#callback for the LED
def led_callback(client, data, msg):

    #convert the data so that the if-else statement will be executed
    data = str(msg.payload, "utf-8")
    
    if (data == "LED_toggle"):
        #print("Test")
        if (digitalRead(led)): #if the LED is currently on
            digitalWrite(led,0) #turn the LED off
        else:
            digitalWrite(led,1) #turn the LED on

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("anrg-pi5/led")
    client.subscribe("anrg-pi5/lcd")

    #add my custom callbacks:

    client.message_callback_add("anrg-pi5/led", led_callback)
    client.message_callback_add("anrg-pi5/lcd", lcd_callback)

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

    # Loop and read the ultrasonic ranger in 1 second intervals
    # and publish the distance values to anrg-pi5/ultrasonicRanger
    # Also monitor the grovepi button

    while True:
        
        t = th02()

        time.sleep(1)

        #read temperature data:
        temp_data = str(t.getTemperature())

        #publish the ultrasonic ranger data
        client.publish("anrg-pi5/temperature", temp_data)

        #read humidity data:
        humid_data = str(t.getHumidity())

        client.publish("anrg-pi5/humidity", humid_data)

