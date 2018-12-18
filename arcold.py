# TODO generare kill per uccidere nuovo processo generato 
# Cosa migliore è creare un altro file python dove metto il counter
# Poi con Popen o file .sh controllo aperture e chiusura di quei processi

import multiprocessing 
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

#define the pins that goes to the circuit
photosensor_pin = 7

#process that always checks the state of the photosensor and eventually count
def runCounter(photosensor_pin, lock):
                    
    #setup gpios
    GPIO.setup(photosensor_pin, GPIO.IN)
                 
    while True:
        counter_trigger = True
        while (GPIO.input(photosensor_pin) == GPIO.HIGH):
             continue           

        #count if needed
        if (counter_trigger):
            lock.acquire()
            counter.value += 1
            lock.release()
            counter_trigger = False
            
if __name__ == "__main__": 
    #Main process to interact with the program        
    try:
        # initial counter (in shared memory) 
        counter = multiprocessing.Value('i', 0)
        
        #lock to access counter shared variable
        lock = multiprocessing.Lock()
        counterProcess = multiprocessing.Process(target=runCounter, args=(photosensor_pin, lock)) 
        counterProcess.start()
        
        # Main loop
        while True:
            cmd = input("Pass a command among \"Count\" \"Exit\"")
            if (cmd == "Count"):
                lock.adquire()
                print("Counter value is {0}".format(counter.value))
                lock.release()
            if (cmd == "Exit"):
                #TODO save the context
                break
               
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
