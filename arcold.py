from time import sleep
import sys
import paho.mqtt.client as mqtt
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from db import *
from util import *
from form import ProgramForm
from flask import Flask
import os

client = connect_client("Server")
#app in Flask
app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='arcold-dev',
        DATABASE=os.path.join(app.instance_path, 'arcold.db'),
    )

@app.route('/')
def index():
    init_db()
    db = get_db()
    cages = db.execute(
        'SELECT *'
        'FROM cages'
    ).fetchall()

    return render_template('arcold/index.html', cages=cages)


@app.route('/cage/<int:id>', methods=('GET', 'POST'))
def cage_details(id):
    from datetime import datetime

    cage = get_cage(id)
    form = ProgramForm()
    if request.method == 'POST':
        res = request.form
        start = compute_timestamp(res['start_time'])
        final = compute_timestamp(res['final_time'])
        insert_program_events(start, final, id)

        #send message to the next cage
        print("Sending the message to "+cage[1])
        
        send_prog_event(client, cage[1], start, final)
        #send_message(client, cage[1], "next {0} {1}".format(start, final))

    #select licking_events
    counter = licking_event_selection_counter(id)
    list_licks = licking_event_selection(id)
    final_list = []
    for event in list_licks:
        final_list += [(datetime.fromtimestamp(event[1]).ctime(), datetime.fromtimestamp(event[2]).ctime())]

    #select running program_event
    prog = cant_drink(id)
    event = ""
    if (not prog[1]):
        event = "No event programmed"
    else:
        event = "The cage is blocked until {0}".format(datetime.fromtimestamp(prog[0][2]).ctime())
    return render_template('arcold/cage.html', cage=cage, counter=counter, list_licks=final_list[-5:], form=form, event=event)



if __name__ == '__main__':
    send_message(client, "Server", "Ciao")
    #counterProcess = multiprocessing.Process(target=runCounter, args=(photosensor_pin, lock))
    #counterProcess.start()
    sleep(1)
    app.run(host='0.0.0.0')
