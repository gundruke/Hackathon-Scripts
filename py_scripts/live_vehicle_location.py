import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random

#load each file in the directory

THINGSBOARD_HOST = 'localhost'
vehicles = ['first1','first2']

data = []
sensor_data = {}
for filename in os.scandir('routes'):
    with open(filename.path, 'r') as f:
        data.append(json.load(f))

counter = 0
while True:


        for i in range(len(vehicles)):
            client = mqtt.Client()
            client.username_pw_set(vehicles[i])

            client.connect(THINGSBOARD_HOST, 8081, 60)
            client.loop_start()

#            print(f"lat: {i['latitude']}, long: {i['longitude']}")
            sensor_data['latitude'] = data[i][counter%len(data[i])]['latitude']
            sensor_data['longitude'] = data[i][counter%len(data[i])]['longitude']
            client.publish('v1/devices/firstresponderpost/telemetry', json.dumps(sensor_data), 1)
            time.sleep(0.5)
        counter+=1


# Set access token


# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval



# lat:   40.641841 - 40.6246665863825
# long:  -8.656439 - -8.65726089425152

