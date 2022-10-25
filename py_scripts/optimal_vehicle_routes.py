import logging
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException
import paho.mqtt.client as mqtt
import time

import json

import sys
from pyrosm import OSM
import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt

osm=OSM("map.pbf")


def node_dict_generator(nodes):

    dict_node={}
    for index, row in nodes.iterrows():
        dict_node[row["id"]]=(row["lon"],row["lat"])

    return dict_node


nodes, edges = osm.get_network(nodes=True, network_type="driving")
node_dict=node_dict_generator(nodes)
G = osm.to_graph(nodes, edges, graph_type="networkx")



def get_traffic_weights(num_edges):
    return [1] * num_edges


def get_optimal_route(graph, start_coords, end_coords):
    nx.set_edge_attributes(graph, "traffic", get_traffic_weights)

    source_node=ox.distance.nearest_nodes(G, start_coords[0], start_coords[1])
    end_node=ox.distance.nearest_nodes(G, end_coords[0], end_coords[1])

    optimal_path_nodes = nx.shortest_path(graph, source_node, end_node, weight="traffic")
    route_coords=[]
    for road in optimal_path_nodes:
        route_coords.append(node_dict[road])


    return route_coords





# ThingsBoard REST API URL
url = "http://localhost:8080"
# Default Tenant Administrator credentials
username = "EMAIL_HERE"
password = "PASSWORD_HERE"


def on_message(client, userdata, message):
    print("data received")
    data =json.loads(message.payload.decode("utf-8"))

    with RestClientCE(base_url=url) as rest_client:
        try:
            rest_client.login(username=username, password=password)
            user = rest_client.get_user()
            print("Logged in as %s %s" % (user.first_name, user.last_name))
            # devices = rest_client.get_customer_dev??ice_infos(customer_id=CustomerId('CUSTOMER', user.id), page_size=str(10),
            #                                                 page=str(0))
            found_device = rest_client.get_device_by_id(device_id=data['id']['id'])
            print(found_device)
            incident = rest_client.get_attributes(found_device.id)
            print(incident)
            # res = rest_client.get_attributes_by_scope('DEVICE', DeviceId('DEVICE', found_device.id), 'SERVER_SCOPE')
            incident_loc = (incident[3]['value'],incident[4]['value'])
            incident_loc = (-8.661532519848219,40.63139785452397)
            pd = (-8.648849, 40.6318261)
            hospital = (-8.6553876,  40.6349828)

            pd_ghost = get_optimal_route(G, pd, incident_loc)
            pd_ghost.extend(get_optimal_route(G, incident_loc, hospital))

            print(pd_ghost)
            THINGSBOARD_HOST = 'localhost'
            ACCESS_TOKEN = 'TOKEN_HERE'

            # Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
            INTERVAL = 3 * 60

            sensor_data = {'longitude': 0, 'latitude': 0}

            next_reading = time.time()

            client = mqtt.Client()

            # Set access token
            client.username_pw_set(ACCESS_TOKEN)

            # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
            client.connect(THINGSBOARD_HOST, 8081, 60)

            client.loop_start()

            try:
                while True:
                    for i in pd_ghost:
                        sensor_data['latitude'] = i[1]
                        sensor_data['longitude'] = i[0]
                        client.publish('v1/ghosts/telemetry', json.dumps(sensor_data), 1)
                        time.sleep(0.01)
                    for i in reversed(pd_ghost):
                        sensor_data['latitude'] = i[1]
                        sensor_data['longitude'] = i[0]
                        client.publish('v1/ghosts/telemetry', json.dumps(sensor_data), 1)
                        time.sleep(0.01)
                    time.sleep(30)
            except KeyboardInterrupt:
                pass

            client.loop_stop()
            client.disconnect()






        except ApiException as e:
            logging.exception(e)



mqttBroker ="localhost"

client = mqtt.Client()
client.connect(mqttBroker, 1884, 1000)

client.loop_start()

client.subscribe("incident/created")
client.on_message=on_message

time.sleep(30)
client.loop_stop()










#mqttt in


#logic

#Mqtt out

