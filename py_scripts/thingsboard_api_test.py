import logging
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
url = "http://mednat.ieeta.pt:8791"
# Default Tenant Administrator credentials
username = "USERNAME_HERE"
password = "PASSWORD_HERE"

print("here")
with RestClientCE(base_url=url) as rest_client:
    try:
        rest_client.login(username=username, password=password)
        user = rest_client.get_user()
        print("Logged in as %s %s" % (user.first_name, user.last_name))
        # devices = rest_client.get_customer_dev??ice_infos(customer_id=CustomerId('CUSTOMER', user.id), page_size=str(10),
        #                                                 page=str(0))
        found_device = rest_client.get_device_by_id(device_id='DEVICE_ID')
        print(found_device)
        rests = rest_client.get_attributes(found_device.id)
        print(rests)
        # res = rest_client.get_attributes_by_scope('DEVICE', DeviceId('DEVICE', found_device.id), 'SERVER_SCOPE')


        print(res)

        # print("Device info:\n%r", res)
    except ApiException as e:
        logging.exception(e)
