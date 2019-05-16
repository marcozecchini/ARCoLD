import paho.mqtt.client as mqtt
from db import look_for_cage, insert_licking_events, get_next_prog
from time import sleep
#broker address
BROKER_ADDR = "128.40.51.144"
client = None

def connect_client(name_client):
    client = mqtt.Client(name_client)
    client.on_message = on_message
    client.connect(BROKER_ADDR)

    client.loop_start()
    client.subscribe("arcold/"+name_client)
    return client

def send_message(client, client_dest, msg):
    client.publish("arcold/"+client_dest, msg)

def disconnect_client(client):
    client.loop_stop()

def on_message(client, userdata, message):
    print("On "+ message.topic + ": ["+ str(client._client_id)+"]-> "  +  str(message.payload))
    pars = message.payload.split(" ")
    if "active" in pars[0]:
        #print("In active")
        id = look_for_cage(pars[1])
        
        send_message(client, pars[1], "confirm {0}".format(id))
        sleep(2)
        send_progs(client, id, pars[1])

    elif "lick" in pars[0]:
        insert_licking_events(pars[1], pars[2], pars[3])
        print("Received a lick event")


def send_progs(client, cage_id, cage_name):
    
    progs = get_next_prog(cage_id)
    res = "prog"
    
    for item in progs:
        #it = item.split(", ")
        res += " "
        res += str(item[1])+" "+ str(item[2])
    
    send_message(client, cage_name, res)

def compute_timestamp(start_str):
    from datetime import datetime
    temp = start_str.split(",")
    dates = temp[0].split("/")
    hours = temp[1].split(":")
    start = (datetime(year=int(dates[2]), month=int(dates[1]), day=int(dates[0]), hour=int(hours[0]), minute=int(hours[1])) - datetime.fromtimestamp(0)).total_seconds()
    return start

def send_prog_event(client, name, start, end):
    send_message(client, name, "next {0} {1}".format(start, end))
