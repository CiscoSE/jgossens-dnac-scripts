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
#Standard library imports.
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning
'''
#Standard library imports.
from os import environ
import requests
import json
import os
import argparse
import re
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning

#Related third party imports.
from webexteamssdk import WebexTeamsAPI
from dnacentersdk import api
from flask import Flask, jsonify, request

#Local application/library specific imports.
import constants as c

# Disable 'Insecure Connection' warning for DNA-C
urllib3.disable_warnings(InsecureRequestWarning)

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--site', default='')
args = parser.parse_args()

# Variables
site_name = args.site

dnac = api.DNACenterAPI(username=c.DNAC_FRA2_USERNAME,
                        password=c.DNAC_FRA2_PASSWORD,
                        base_url=c.DNAC_FRA2_URL,
                        version=c.DNAC_FRA2_VERSION,
                        verify=False)


# Find the site and extract the unique site id for later usage
sites = dnac.sites.get_site()
for s in sites.response:
    if(s.name == site_name):
        site = s
site_id = site.id

# The membership API takes a location and returns a big JSON file of all sub-locations and devices that are member of this location
url = '/dna/intent/api/v1/membership/' + site_id
members = dnac.custom_caller.call_api('GET', url)

print('Switches found in ' + site_name +  ':')

# Iterate all the devices that are member of our location
num_int_sum = 0
num_int_down = 0
for m in members.device:
    for device in m.response:
        device_id = device.instanceUuid
        hostname = device.hostname
        status = device.reachabilityStatus
        int_count = device.interfaceCount

        print('\nSwitch: ' + hostname)
        print('Status: ' + status)

        count = 0
        url_int = 'dna/intent/api/v1/interface/network-device/{}'.format(device_id)
        interfaces = dnac.custom_caller.call_api('GET', url_int)
        
        if(status == 'Reachable'):
            for i in interfaces.response:
                if(i.status == 'down'):
                    num_int_down += 1
                    num_int_sum +=1
                else:
                    num_int_sum +=1

        if(status == 'Unreachable'):
            for i in interfaces.response:
                    num_int_down += 1
                    num_int_sum +=1
        
print('===========================')
print('Location: ' + site_name)
print('Interfaces total: ' + str(num_int_sum))
print('Interfaces down: ' +str(num_int_down))
print(str(round((num_int_down / num_int_sum)*100,2)) + '% of all interfaces down')

