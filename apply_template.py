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
parser.add_argument('--site', default='')
parser.add_argument('--tmpl', default='')
parser.add_argument('--var', default='')
args = parser.parse_args()

# Variables
site_name = args.site
site_name = args.site
src_int = args.var
tmpl_name = args.tmpl

# Find the template and extract the unique template ID for later usage
templates = dnac.template_programmer.gets_the_templates_available()
for t in templates:
    if(t.name == tmpl_name):
        tmpl_id = t.templateId

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
for m in members.device:
    for device in m.response:
        device_id = device.instanceUuid
        hostname = device.hostname
        
        print('\nSwitch: ' + device.hostname)
        
        try:
            # Get the IP address of the correct interface so that we can feed this information to the IP SLA template
            url_int = 'dna/intent/api/v1/interface/network-device/{}/interface-name?name={}'.format(device_id, src_int)
            interface = dnac.custom_caller.call_api('GET', url_int)
            src_ip = interface.response.ipv4Address
            print('Loopback10 IPv4: ' + src_ip)

            # Create the JSON data that we need to send via http POST to Cisco DNA Center
            # Documentation of the dnacentersdk describes how this has to look like
            data = {'forcePushTemplate' : True, 'targetInfo' : [{'hostName' : hostname, 'id' : device_id, 'params': {'source-ip': src_ip},'type' : 'MANAGED_DEVICE_UUID'}], 'templateId' : tmpl_id}
            payload = json.dumps(data)
   
            # API Call to Cisco DNA Center to apply the template to the switch
            url_tmpl = 'dna/intent/api/v1/template-programmer/template/deploy'
            response = dnac.custom_caller.call_api('POST', url_tmpl, data=payload)
        except:
            print('Something went wrong - does the switch have a Loopback 10 interface?')