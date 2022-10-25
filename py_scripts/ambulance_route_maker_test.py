import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random


with open('data.json', 'r') as f:
    data = json.load(f)



print(data[0])
THINGSBOARD_HOST = 'localhost'
ACCESS_TOKEN = 'KDvHf0BgfXT2Niv5fa8m'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=3*60

sensor_data = {'longitude': 0, 'latitude': 0}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 8081, 60)

client.loop_start()

#lat: 	40.641841 - 40.6246665863825
#long: 	-8.656439 - -8.65726089425152


try:
    while True:
        for i in data:
            print(f"lat: {i['latitude']}, long: {i['longitude']}")
            sensor_data['latitude'] = i['latitude']
            sensor_data['longitude'] = i['longitude']
            client.publish('v1/devices/ambulance/ghost/telemetry', json.dumps(sensor_data), 1)
            time.sleep(0.05)            
        for i in reversed(data):
            print(f"lat: {i['latitude']}, long: {i['longitude']}")
            sensor_data['latitude'] = i['latitude']
            sensor_data['longitude'] = i['longitude']
            client.publish('v1/devices/ambulance/ghost/telemetry', json.dumps(sensor_data), 1)
            time.sleep(0.05)
        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

