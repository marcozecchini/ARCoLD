import multiprocessing 
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

#define the pins that goes to the circuit
photosensor_pin = 7




#process that always checks the state of the photosensor and eventually count
def runCounter(photosensor_pin, lock):
    camera = PiCamera
    #update pid value
    lock.acquire()
    pid.value = os.getpid()
    print("Counter process has pid {0}".format(pid.value))
    lock.release()
    
    #setup gpios
    GPIO.setup(photosensor_pin, GPIO.IN)
                 
    while True:
        counter_trigger = True
        while (GPIO.input(photosensor_pin) == GPIO.LOW): #it should be HIGH
             continue           

        #count if needed
        if (counter_trigger):
            lock.acquire()
            counter.value += 1
            lock.release()
            
            #take the photo to confirm
            camera.start_preview()
            sleep(1) # see if it takes photo without delay
            camera.capture('home/pi/Documents/giulio/ARCoLD/photos/image'+str(time.time())+'.jpg')
            camera.stop_preview()
            
            counter_trigger = False
            
if __name__ == "__main__": 
    #Main process to interact with the program        
    try:
        # initial counter (in shared memory) 
        counter = multiprocessing.Value('i', 0)
        
        # counter pid (in shared memory)
        pid = multiprocessing.Value('i', 0)
        
        #lock to access counter shared variable
        lock = multiprocessing.Lock()
        counterProcess = multiprocessing.Process(target=runCounter, args=(photosensor_pin, lock)) 
        counterProcess.start()
        sleep(1)
        # Main loop
        while True:
            cmd = raw_input("Pass a command among \"Count\", \"Suspend\", \"Exit\":\t")
            if (cmd == "Count"):
                lock.acquire()
                print("Counter value is {0}".format(counter.value))
                lock.release()
            if (cmd == "Suspend"):
				os._exit(os.EX_OK)
            if (cmd == "Exit"):
				counterProcess.terminate()
				break
               
    except KeyboardInterrupt:
        pass
        
