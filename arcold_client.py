import socket
from util import send_socket, receive_socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 3000))
MSGLEN = 1024

try:
	while True:
		cmd = raw_input("Pass a command among \"Count\", \"Reset\", \"Suspend\",\"List\", \"Exit\":\t")
		send_socket(client_socket, cmd)
		data = receive_socket(client_socket)
		print(data)
		if (cmd == "Suspend" or cmd == "Exit"):
			client_socket.close()
			break
except KeyboardInterrupt:
	send_socket(client_socket, "Suspend")
	client_socket.close()
