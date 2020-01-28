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

devices = dnac.devices.get_device_list()

for device in devices.response:
    print(device.hostname)
    print(device.platformId)
    print(device.managementIpAddress)
    print(device.serialNumber)

    print()

