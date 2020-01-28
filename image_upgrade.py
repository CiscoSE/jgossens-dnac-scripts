#!/usr/bin/env python3
'''
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

#Standard library imports.
import argparse
import requests
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning

#Related third party imports.
from dnacentersdk import api

#Local application/library specific imports.
import constants as c

# Disable 'Insecure Connection' warning for DNA-C
urllib3.disable_warnings(InsecureRequestWarning)

dnac = api.DNACenterAPI(username=c.DNAC_FRA2_USERNAME,
                        password=c.DNAC_FRA2_PASSWORD,
                        base_url=c.DNAC_FRA2_URL,
                        version=c.DNAC_FRA2_VERSION,
                        verify=False)


# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--ios', default='')
parser.add_argument('--switch', default='')
args = parser.parse_args()

# Variables
switch = args.switch #'C3650-Telekom.fra-lab.net'
ios = args.ios #'16.9.3a'
    
# Use IOS version 16.9.3, find the image in DNA-C and store the image id for later usage
id_img = None
url_img = 'dna/intent/api/v1/image/importation'
images = dnac.custom_caller.call_api('GET', url_img)
for i in images.response:
    if(i.name == ios):
        id_img = i.imageUuid
        print('Specified Image found')

# Use only one test switch specified by hostname, find it in DNA-C and store switch id for later usage
# Note: The example above uses the "call_api" method of dnacentersdk and hence the API URI is manually specified. This way we work very close to the API documentation.
# In this example we use a predefined function "get_device_list" of dnacentersdk which hides these details from us and simply returns the devices, therefore its shorter.
# The same result could also be achieved by using the call_api again and specify the API URI yourself.
id_dev = None
devices = dnac.devices.get_device_list()
for d in devices.response:

    if(d.hostname == switch):
        id_dev = d.id
        print('Specified Switch found')

# Distribute the specified IOS image from DNA-Center to the specified switch
url_dist = 'dna/intent/api/v1/image/distribution'
data = [{'deviceUuid' : id_dev, 'imageUuid' : id_img}]
payload_dist = json.dumps(data)
dist = dnac.custom_caller.call_api('POST', url_dist, data=payload_dist)
print('Distributing Image to Switch, Response:')
print(dist)

# Install the image on the switch
url_act = 'dna/intent/api/v1/image/activation/device'
data = [{'deviceUuid' : id_dev, 'imageUuidList' : [id_img]}]
payload_act = json.dumps(data)
print('Installing Image to Switch, Response:')
act = dnac.custom_caller.call_api('POST', url_act, data=payload_act)
print(act)
   


