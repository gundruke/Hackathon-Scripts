import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random


THINGSBOARD_HOST = 'localhost'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL = 3 * 60

data = []

with open('locations/data.json', 'r') as f:
    data = json.load(f)

sensor_data = {}
next_reading = time.time()
client = mqtt.Client()

try:
    while True:

        #generate data
        #temperature
        #co2
        #o2
        #Humidity


        #same in all sensors
        #wind
        #wind direction



        #generate random wind
        wind = random.randint(0, 50) #km/h
        wind_direction = random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

        for i in range(1,65):
            # generate random data
            client.username_pw_set(f"Sensor_hub_{str(i).zfill(2)}")

            print(f"Sensor_hub_{str(i).zfill(2)}")

            # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
            client.connect(THINGSBOARD_HOST, 8081, 60)

            client.loop_start()

            sensor_data['temperature'] = random.randint(15.0, 50.0)
            sensor_data['co2'] = random.randint(400, 5000)
            sensor_data['o2'] = random.randint(0, 100)  # below 19% is dangerous for humans
            sensor_data['humidity'] = random.randint(0, 100)
            sensor_data['wind'] = wind
            sensor_data['wind_direction'] = wind_direction
            sensor_data['longitude'] = data[i-1]['longitude']
            sensor_data['latitude'] = data[i-1]['latitude']
            client.publish('v1/devices/sensorhub/telemetry', json.dumps(sensor_data), 1)
            print(sensor_data)

#            client.disconnect()

            time.sleep(0.2)
        time.sleep(5)


        #send data1


except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

