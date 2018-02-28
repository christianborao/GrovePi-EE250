# LED Client 
# This code sends requests to the Raspberry Pi to turn on and
#off the Grove LED using TCP packets.

import socket

def Main():
	host = '10.0.2.15' #VM address
	port = 9000

	s = socket.socket()

	data = input("-> ")
	server = ('192.168.1.199', int(9000))
	s.connect(server)

	while data != 'q':

		s.sendto(data.encode('utf-8'), server)
		data = input("-> ")
	s.close()

if __name__ == '__main__':
		Main()
