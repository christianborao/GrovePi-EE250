#Ultrasonic Sensor Server
#
# This code runs on your VM and receives a stream of packets holding ultrasonic
# sensor data and prints it to stdout. Use a UDP socket here.

import grovepi
import socket

ultrasonic_ranger = 4

def Process_Ultrasonic():
	host = '10.0.2.15'
	port = 9000

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(host,port)

	print("Server Started!")

while True:
	try:

		print(grovepi.ultrasonicRead(ultrasonic_ranger))

	except TypeError:
		print("Error")
	except IOError:
		print("Error")
	c.close()

if __name__ == '__main__'
	Process_Ultrasonic()