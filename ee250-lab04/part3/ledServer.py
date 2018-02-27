# LED Server
# 
# This program runs on the Raspberry Pi and accepts requests to turn on and off
# the LED via TCP packets.

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('Christian/GrovePi-EE250/Software/Python/')

from grovepi import *

# use TCP
import socket
import time


led = 2

pinMode(led, "OUTPUT")

def Main():

	host = '192.168.1.199' #pi
	port = 9000

	s = socket.socket()
	s.bind((host,port))
	s.listen(1)

	client, address = s.accept()

	print("Connection with address: " + str(address))

	while True:
		data = client.recv(1024).decode('utf-8')
		if(data == "LED_ON"):
			digitalWrite(led,1)
			print ("LED_ON Success")
		elif(data == "LED_OFF"):
			digitalWrite(led,0)
			print("LED_OFF Success")
		else:
			break
	s.close()

if __name__ == '__main__':
		Main()