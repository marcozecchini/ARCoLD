import paho.mqtt.client as mqtt
from db import look_for_cage, insert_licking_events
#broker address
BROKER_ADDR = "128.40.51.144"
client = None

def connect_client(name_client):
    client = mqtt.Client(name_client)
    client.on_message = on_message if name_client == "Server" else on_message_client
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
        print("In active")
        id = look_for_cage(pars[1])
        print(id)
        send_message(client, pars[1], "confirm {0}".format(id))

    elif "lick" in pars[0]:
        insert_licking_events(pars[1], pars[2], pars[3])



def on_message_client(client_instance, userdata, message):
    print("On " + message.topic + ": [" + str(client_instance._client_id) + "]-> " + str(message.payload))
    pars = message.payload.split(" ")

    if "prog" in pars[0]:
        try:
            from client import next_prog
            i = 1
            while i < len(pars):
                next_prog += [[ float(pars[i]), float(pars[i+1]) ]]
                i += 2
        except:
            print("--> Something wrong in the pass of data")

    elif "next" in pars[0]:
        try:
            from client import next_prog
            next_prog += [[ float(pars[1]), float(pars[2]) ]]
        except:
            print("--> Something wrong in passing data from 'next' command")

    elif "confirm" in pars[0]:
        try:
            import client as cl
            cl.cage_id = int(pars[1])
        except:
            print("--> Something wrong in passing data from 'confirm' command")

def compute_timestamp(start_str):
    from datetime import datetime
    temp = start_str.split(",")
    dates = temp[0].split("/")
    hours = temp[1].split(":")
    start = (datetime(year=int(dates[2]), month=int(dates[1]), day=int(dates[0]), hour=int(hours[0]), minute=int(hours[1])) - datetime.fromtimestamp(0)).total_seconds()
    return start

def send_prog_event(client, start, end):
    send_message(client, "Server", "next {0} {1}".format(start, end))
