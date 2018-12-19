import socket 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 3000))

try:
	while True:
		cmd = raw_input("Pass a command among \"Count\", \"Reset\", \"Suspend\",\"List\", \"Exit\":\t")
		client_socket.sendall(cmd)
		data = client_socket.recv(1024)
		print(data)
		if (cmd == "Suspend" or cmd == "Exit"):
			client_socket.close()
			break
except KeyboardInterrupt:
	client_socket.sendall("Suspend")
	client_socket.close()
