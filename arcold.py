import multiprocessing 
import RPi.GPIO as GPIO
from picamera import PiCamera
from flask import Flask
import os
import sys
from datetime import datetime
import time
import socket
from time import sleep
from util import send_socket, receive_socket, send_help
from flaskr.db import insert_licking_events


GPIO.setmode(GPIO.BCM)
app = Flask(__name__)

#define the pins that goes to the circuit
photosensor_pin = 4

#process that always checks the state of the photosensor and eventually count
def runCounter(photosensor_pin, lock, file_event):
    camera = PiCamera()
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
        start_time = time.time()
       
        camera.start_preview()
        #sleep(1) # see if it takes photo without delay
        camera.capture('photos/image/'+str(datetime.fromtimestamp(start_time))+'.jpg')
        camera.stop_preview()
        
        print(datetime.fromtimestamp(start_time))
        if (time_bound.value < start_time):
			time_bound.value = 0
			GPIO.output(output_pin, GPIO.HIGH) 
		
		else:
			print("At "+str(datetime.fromtimestamp(start_time))+" it tries to lick, but it's blocked")
			
        counter.value += 1
        
        while(GPIO.input(photosensor_pin) == GPIO.HIGH):
			pass
		
        final_time = time.time()
        print(datetime.fromtimestamp(final_time))
        
        #insert into db
        insert_licking_events(start_time, final_time, "1") #1 per ora, con più gabbie più di uno
        
        GPIO.output(output_pin, GPIO.LOW)
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
		 
    except KeyboardInterrupt:
        counterProcess.join()
        server_socket.close()
    except TypeError:
		server_socket.close()
    finally:
		GPIO.cleanup(17)
