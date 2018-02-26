# LED Client 
#
# This code sends requests to the Raspberry Pi to turn on and
#off the Grove LED using TCP packets.

import socket

def Main():
	host = '10.0.2.15' #VM address
	port = 9000

	s = socket.socket()
	s.connect((host,port))

	data = input("-> ")

	while data != 'q':
		s.send(message.encode('utf-8'))
		message = input("-> ")
	s.close()

if __name__ == '__main__':
		Main()