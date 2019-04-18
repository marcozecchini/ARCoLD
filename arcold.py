from time import sleep

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from db import *
from flask import Flask
import os


#define the pins that goes to the circuit
photosensor_pin = 4

#app in Flask
app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='arcold-dev',
        DATABASE=os.path.join(app.instance_path, 'arcold.db'),
    )

@app.route('/hello')
def hello():
    return 'hello'

@app.route('/')
def index():
    init_db()
    db = get_db()
    cages = db.execute(
        'SELECT *'
        'FROM cages'
    ).fetchall()

    return render_template('arcold/index.html', cages=cages)


def get_cage(id):
    cage = get_db().execute(
        '''SELECT * FROM cages WHERE id={0}'''.format(id)
    ).fetchone()
    if cage is None:
        abort(404, "Cage id {0} doesn't exist.".format(id))

    return cage


# @bp.route('cage/<int:id>', methods=('GET', 'POST'))
@app.route('/cage/<int:id>')
def cage_details(id):
    cage = get_cage(id)

    counter = licking_event_selection_counter(id)

    return render_template('arcold/cage.html', cage=cage, counter=counter)


def runCounter(photosensor_pin, lock):
    # camera = PiCamera()
    # update pid value
    lock.acquire()
    # pid.value = os.getpid()
    # print("Counter process has pid {0}".format(pid.value))
    lock.release()
    output_pin = 17

    # setup gpios
    # GPIO.setup(photosensor_pin, GPIO.IN)
    # GPIO.setup(output_pin, GPIO.OUT)

    while True:
        while True:
            pass
        # while (GPIO.input(photosensor_pin) == GPIO.LOW): #it should be HIGH
        #    counter_trigger = True

        # count if needed

        print("Licking event...")
        lock.acquire()
        start_time = time.time()

        # camera.start_preview()
        # sleep(1) # see if it takes photo without delay
        # camera.capture('photos/image/'+str(datetime.fromtimestamp(start_time))+'.jpg')
        # camera.stop_preview()

        print(datetime.fromtimestamp(start_time))
        if (time_bound.value < start_time):
            time_bound.value = 0
        # GPIO.output(output_pin, GPIO.HIGH)
        else:
            print("At " + str(datetime.fromtimestamp(start_time)) + " it tries to lick, but it's blocked")

        counter.value += 1

        # while(GPIO.input(photosensor_pin) == GPIO.HIGH):
        #    pass

        final_time = time.time()
        print(datetime.fromtimestamp(final_time))

        # insert into db
        insert_licking_events(start_time, final_time, "1")  # 1 per ora, con più gabbie più di uno

        # GPIO.output(output_pin, GPIO.LOW)
        lock.release()
        print("OFF")

if __name__ == '__main__':
    # lock to access counter shared variable
    lock = multiprocessing.Lock()
    counterProcess = multiprocessing.Process(target=runCounter, args=(photosensor_pin, lock))
    counterProcess.start()
    sleep(1)
    app.run()
