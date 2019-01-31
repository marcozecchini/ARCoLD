End="END"
Help_message="""
- \"Count\" returns the status of the system
- \"List\" returns the occurrences logged in a file
- \"Prog\" is used to program a timespan where the mice cannot drink
\tIt must be followed by \"-span=\"and a number of hours 
\tthat the pump remains disabled
- \"Reset\" cleans the log
-  \"Remove\" cleans the programmation
- \"Suspend\" close the connection with the server
- \"Exit\" close both the connection and the server
"""

def send_help(sock):
	send_socket(sock, Help_message)

def send_socket(sock, msg):
	# Prefix each message with a 4-byte length (network byte order)
    sock.sendall(msg+End)
	
def receive_socket(sock):
    total_data=[]
    data=''
    while True:
		data=sock.recv(8192)
		if End in data:
			total_data.append(data[:data.find(End)])
			break
		total_data.append(data)
		if len(total_data)>1:
			#check if end_of_data was split
			last_pair=total_data[-2]+total_data[-1]
			if End in last_pair:
				total_data[-2]=last_pair[:last_pair.find(End)]
				total_data.pop()
				break
    return ''.join(total_data)

