import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ="localhost"

client = mqtt.Client()
client.connect(mqttBroker, 1884)

client.loop_start()

client.subscribe("incident/created")
client.on_message=on_message

time.sleep(30)
client.loop_stop()
