import socket 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 3000))
while True:
	cmd = raw_input("Pass a command among \"Count\", \"Suspend\", \"Exit\":\t")
	client_socket.sendall(cmd)
	data = client_socket.recv(256)
	print(data)
	if (cmd == "Suspend"):
		client_socket.close()
		break
