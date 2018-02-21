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

	host = '192.168.1.203'
	port = 1024

	server_addr = '192.168.1.144'

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(host,port)

	while True:

		server = (server_addr, int(dst_port))
		s.sendto(grovepi.ultrasonicRead(ultrasonic_ranger), server)
		dst_port = 8000

	s.close()

if __name__ == '__main__'
	Main()
