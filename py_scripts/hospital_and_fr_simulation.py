import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random

# load each file in the directory

THINGSBOARD_HOST = 'localhost'
locations = ['first1', 'first2', 'first3', 'first4', 'hospital1', 'hospital2', 'hospital3']
mqtt_data = ['firstresponderpost', 'firstresponderpost', 'firstresponderpost', 'firstresponderpost', 'hospital', 'hospital',
        'hospital']

data = []
sensor_data = {}

with open('locations/data.json', 'r') as f:
    data = json.load(f)

counter = 0
while True:
    for i in range(len(locations)):
        client = mqtt.Client()
        client.username_pw_set(locations[i])

        client.connect(THINGSBOARD_HOST, 8081, 60)
        client.loop_start()

        sensor_data = data[i]

        client.publish(f'v1/devices/{mqtt_data[i]}/telemetry', json.dumps(sensor_data), 1)
        time.sleep(120)
    counter += 1

# Set access token


# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval


# lat:   40.641841 - 40.6246665863825
# long:  -8.656439 - -8.65726089425152
