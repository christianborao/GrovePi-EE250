# Ultrasonic Sensor Client
# 
# This code runs on the Raspberry Pi. It should sit in a loop which reads from
# the Grove Ultrasonic Ranger and sends the reading to the Ultrasonic Sensor 
# Server running on your VM via UDP packets. 

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are able to successfully `import grovepi`
sys.path.append('../../Software/Python/')

import grovepi
import socket

def Main():

	ultrasonic_ranger = 4

	host = '192.168.1.199' #RPI address
	port = 5000

	server_addr = '192.168.1.140' # OS address

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,port))

	dst_port = 8000

	while True:

		server = (server_addr, int(dst_port))
		data = str(grovepi.ultrasonicRead(ultrasonic_ranger))

		data = data.encode('utf-8')
		s.sendto(data, server)
		print(data)

	s.close()

if __name__ == '__main__':
	Main()
