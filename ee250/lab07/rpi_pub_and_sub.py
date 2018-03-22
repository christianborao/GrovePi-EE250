"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time

import sys
sys.path.append('../../Software/Python/')

from grovepi import *
from grove_rgb_lcd import *

#I gave the ports names based on what was connected to them

#Note the grovepi seems to automatically know where the LCD is
#connected to, so I did not code the LCD port at all 

led = 2
button = 3
ultrasonic_ranger = 4

#set LED port as an output and the button port as an input
pinMode(led, "OUTPUT") 
pinMode(button, "INPUT")


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
    
    if (data == "LED_ON"):
        print("Test")
        digitalWrite(led,1) #turns the LED on
    elif (data == "LED_OFF"):
        digitalWrite(led, 0) #turns the LED off


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
        
        
        time.sleep(1)

        #read ultrasonic ranger data:
        data = str(ultrasonicRead(ultrasonic_ranger))

        #publish the ultrasonic ranger data
        client.publish("anrg-pi5/ultrasonicRanger", data)

        #monitor the button:
        button_status = digitalRead(button)

        #if the button is pressed, publish the string "Button pressed!"
        if (button_status):
            client.publish("anrg-pi5/button", "Button pressed!")




