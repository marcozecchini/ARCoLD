import multiprocessing 
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
import sys
from datetime import datetime
import time
import socket
from time import sleep
from util import send_socket, receive_socket, send_help


GPIO.setmode(GPIO.BCM)

#define the pins that goes to the circuit
photosensor_pin = 4

#process that always checks the state of the photosensor and eventually count
def runCounter(photosensor_pin, lock, file_event):
    #camera = PiCamera()
    #update pid value
    lock.acquire()
    pid.value = os.getpid()
    print("Counter process has pid {0}".format(pid.value))
    lock.release()
    output_pin = 17
    
    #setup gpios
    GPIO.setup(photosensor_pin, GPIO.IN)
    GPIO.setup(output_pin, GPIO.OUT)
	
    while True:
        
        while (GPIO.input(photosensor_pin) == GPIO.LOW): #it should be HIGH           
			counter_trigger = True
			
        #count if needed
        
        print("Licking event...")
        lock.acquire()
        file_event = open("event_list.txt", "a+")
        start_time = time.time()
        print(datetime.fromtimestamp(start_time))
        if (time_bound.value < start_time):
			time_bound.value = 0
			GPIO.output(output_pin, GPIO.HIGH) 
		
	else:
                        print("At "+datetime.fromtimestamp(start_time)+" it tries to lick, but it's blocked")
			
        file_event.write(str(datetime.fromtimestamp(start_time)))
        counter.value += 1
        
        while(GPIO.input(photosensor_pin) == GPIO.HIGH):
			pass
		
        final_time = time.time()
        print(datetime.fromtimestamp(final_time))
        file_event.write(str(datetime.fromtimestamp(final_time))+"\n")
        GPIO.output(output_pin, GPIO.LOW)
        file_event.close()
        lock.release()
        print("OFF")
            
if __name__ == "__main__": 
    #Main process to interact with the program
    counterProcess = 0
    server_socket = 0
    try:
		
		file_event = 0
		# initial counter (in shared memory) 
		counter = multiprocessing.Value('i', 0)

		# counter pid (in shared memory)
		pid = multiprocessing.Value('i', 0)
		# number of hours where the 
		time_bound = multiprocessing.Value('d', 0)
		
		#lock to access counter shared variable
		lock = multiprocessing.Lock()
		counterProcess = multiprocessing.Process(target=runCounter, args=(photosensor_pin, lock, file_event)) 
		counterProcess.start()
		sleep(1)
		
		# socket init
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((socket.gethostname(), 3000))
		server_socket.listen(1)
		print("Waiting for connection...")
		# Main loop
		while True:
			conn, addr = server_socket.accept()
			print("Connection by "+ str(addr))
			cmd = ''
			while True:
				cmd = receive_socket(conn)
				print(str(addr) + " >> " + cmd)
				if (cmd == "Count"):
					lock.acquire()
					send_socket(conn, "- Counter value is {0}.\n- The mice can drink? {1}!".format(counter.value, not time_bound.value > 0))
					lock.release()
				elif (cmd == "List"):
					lock.acquire()
					file_event = open("event_list.txt", "r+")
					data = file_event.read()
					if (data != ""): send_socket(conn, data)
					else: send_socket(conn, ">>> Empty")
					lock.release()
				elif (cmd == "Remove"):
					time_bound.value = 0
					send_socket(conn, "\"Prog\" removed")
				elif ("Prog" in cmd):
					sec_span = (int(cmd.split("-span=")[1])+1) * 3600
					time_bound.value = time.time()+sec_span
					bound = datetime.fromtimestamp(time_bound.value)
					send_socket(conn, "Command \"Prog\" received: it won't drink until "+str(bound))
				elif (cmd == "Reset"):
					lock.acquire()
					file_event = open("event_list.txt", "w+")
					file_event.close()
					counter.value = 0
					lock.release()
					send_socket(conn, "Reset Done!")
				elif (cmd == "Suspend"):
					send_socket(conn, "Closing the connection")
					#server_socket.close()
					cmd = ''
					break
				elif (cmd == "Exit"):
					send_socket(conn, "Closing the connection and exiting")
					server_socket.close()
					counterProcess.terminate()
					sys.exit(0)
				elif(cmd =="Help"):
					send_help(conn)
				else:
					send_socket(conn, "Cmd not recognized")
				cmd = ''
			   
    except KeyboardInterrupt:
        counterProcess.join()
        server_socket.close()
    except TypeError:
		server_socket.close()
        

		#GPIO.output(output_pin, GPIO.HIGH)
		#sleep(1)
		#GPIO.output(output_pin, GPIO.LOW)

		#take the photo to confirm
		#camera.start_preview()
		#sleep(1) # see if it takes photo without delay
		#camera.capture('home/pi/Documents/giulio/ARCoLD/photos/image'+str(time.time())+'.jpg')
		#camera.stop_preview()

		#counter_trigger = False
