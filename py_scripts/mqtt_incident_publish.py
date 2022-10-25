import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random

# load each file in the directory

THINGSBOARD_HOST = 'localhost'


locations = [(-8.648849, 40.6318261), (-8.6553876,  40.6349828), (-8.661532519848219, 40.63139785452397)]
pw = ["pol", "hos", "incidentm"]


data = []
sensor_data = {}

with open('locations/data.json', 'r') as f:
    data = json.load(f)

counter = 0
while True:
    for i in range(len(locations)):
        client = mqtt.Client()
        client.username_pw_set(pw[i])

        client.connect(THINGSBOARD_HOST, 8081, 60)
        client.loop_start()

        sensor_data['latitude'] = locations[i][1]
        sensor_data['longitude'] = locations[i][0]
        client.publish(f'v1/incidentM/telemetry', json.dumps(sensor_data), 1)
        time.sleep(5)
    counter += 1

# Set access token


# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval


# lat:   40.641841 - 40.6246665863825
# long:  -8.656439 - -8.65726089425152

