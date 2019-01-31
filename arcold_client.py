import socket
import re
from util import send_socket, receive_socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 3000))

try:
	while True:
		cmd = raw_input("Pass a command (digit \"Help\" to show the list of commands):\t")
		if ("Prog" in cmd and not re.match("Prog[ \t\n\r\f\v]+-span=[0-9]+\.*[0-9]*", cmd)):
			print(">>> Not a good Prog")
			continue
		send_socket(client_socket, cmd)
		data = receive_socket(client_socket)
		print(data)
		if (cmd == "Suspend" or cmd == "Exit"):
			client_socket.close()
			break
except KeyboardInterrupt:
	send_socket(client_socket, "Suspend")
	client_socket.close()
