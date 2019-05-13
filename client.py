from util import *
from time import sleep
import sys
import time
import RPi.GPIO as GPIO
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)
cage_name = sys.argv[1]
cage_id = 1
server = "Server"
client = connect_client(cage_name)
next_prog = []

'''
    Main loop functions
'''
def runCounter():

    #camera = PiCamera()

    # pins that powers the pump
    output_pin = 17
    # define the pins that goes to the circuit
    photosensor_pin = 4
    
    # setup gpios
    GPIO.setup(photosensor_pin, GPIO.IN)
    GPIO.setup(output_pin, GPIO.OUT)
   
    while True:
        from datetime import datetime

        while (GPIO.input(photosensor_pin) == GPIO.LOW): #it should be HIGH
           counter_trigger = True

        # count if needed

        print("Licking event...")
        start_time = time.time() + 3600

        #camera.start_preview()
        #sleep(1) # see if it takes photo without delay
        #camera.capture('photos/image/'+str(datetime.fromtimestamp(start_time))+'.jpg')
        #camera.stop_preview()

        print(datetime.fromtimestamp(start_time))
        if (available()):
            GPIO.output(output_pin, GPIO.HIGH)
        else:
            print("At " + str(datetime.fromtimestamp(start_time)) + " it tries to lick, but it's blocked")

        while(GPIO.input(photosensor_pin) == GPIO.HIGH):
           pass

        final_time = time.time() + 3600
        print(datetime.fromtimestamp(final_time))

        # send to the db
        send_licking_event(start_time, final_time)

        GPIO.output(output_pin, GPIO.LOW)
        print("OFF")


'''
    Check whether it can drink or not and eventually removes timestamp couples which are already passed.
'''
def available():
    from datetime import datetime
    now = time.time() + 3600
    for couple in next_prog:
        try:
            if  float(couple[1]) < now:
                next_prog.remove([couple[0], couple[1]])
            elif float(couple[0]) < now and float(couple[1]) > now:
                return False
        except:
            print("--> Something went wrong during the check of avalaibility")
    return True

'''
    Function sending licking_event messages
'''
def send_licking_event(start_time, final_time):
    send_message(client, server, "lick {0} {1} {2}".format(start_time, final_time, cage_id))

if __name__ == '__main__':
    try:
        print(cage_name)
        send_message(client, server, "active {0}".format(cage_name))

        sleep(1)
        runCounter()

    except Exception as e:
        print(e)
        disconnect_client(client)
