# Cisco DNA-C Scripts
Simple scripts for Cisco DNA-Center written in Python that show how to utilize APIs and automize / customize several tasks such as Plug and Play (PnP) or Software Image Upgrade (SWIM).

## Table of Contents
* [General info](#general-info)
* [Setup](#setup)

## General info
This project is used to document smaller scripts leveraging the REST APIs of Cisco DNA-Center. The motivation behind this is to demonstrate customers how the APIs work and proof that they are functional in a demo environment. No script contained here underwent any software testing and should not be used in a production environment.
 
## Setup

To run any of the scripts, make sure to install any dependencies via pip:
````
$ pip3 install requests
$ pip3 install dnacentersdk
$ pip3 install http_basic_auth
$ pip3 install argparse
````
Furthermore, in every script, the correct credentials have to be used to login to Cisco DNA-Center. I am using a file ```constants.py``` not contained in this directory that specifies the variables used by the Cisco DNA-Center SDK:

```
import constants as c

dnac = api.DNACenterAPI(username=c.DNAC_FRA2_USERNAME,
                        password=c.DNAC_FRA2_PASSWORD,
                        base_url=c.DNAC_FRA2_URL,
                        version=c.DNAC_FRA2_VERSION,
                        verify=False)
```

Make sure to add this file or to replace the variables in every instance of the call above (usually, there should be one per script). Note that the URL to the Cisco DNA-Center is of the form 'https://IP_OR_URI'

## Scripts

This Section briefly describes what each script is doing and how it is used.

### apply_template.py

Use Case:
The Day N configuration templates that Cisco DNA-Center provides out of the box caused the following two challenges for out customer:
1. The variables specified in the template have to be manually filled from withtin the Cisco DNA-Center Web UI. For a few switches this might be a reasonable action, but if a configuration has to be pushed to 1000 switches, this gets out of hand quickly.
2. In some situations the variables are depending on the current configuration of the corresponding switch. As a specific example we took the following configuration snippet that describes an IP SLA and acts as our Day N template:

Example Day N template: Apply_IP_SLA_2200
```
no ip sla 2200
ip sla 2200
    icmp-echo 10.0.0.1 source-ip ${source-ip}
    owner *** icmp test to router***
    frequency 10
ip sla schedule 2200 life forever start-time now
```

This IP SLA sends an ICMP echo request to the private IP address 10.0.0.1 every ten seconds. The ICMP echo should be sourced from the Loopback10 interface of the switch, so the variable that we have to add is actually the configured loopback's IP address that we have to extract from the running-configuration beforehand. Cisco DNA-Center does not provide this functionality out of the box.

This script receives a site, a Day N template (both have to be known in Cisco DNA-Center already) and the name of an interface as input. For every switch in the site, the script polls the IP address of the interface from Cisco DNA-Center and further instructs it to apply the template specified, whereas the IP address polled acts as the input for the template.

Output of the script are all switches found in the corresponding location and the IP addresses of the specified interface that is taken as the source IP for the IP SLA template.

Example Usage:
```
python3 apply_template.py --site=Dusseldorf --tmpl=Apply_IP_SLA_2200 --var=Loopback10
Switches found in Dusseldorf:

Switch: C9300-Lab
Loopback10 IPv4: 1.1.1.1

```

### compute_interfaces_percentage.py

Use Case:
Our customer asked if it was possible via Cisco DNA-Center to get the percantal value of shutdown interfaces for a specific site. This script receives the site (that is already known to Cisco DNA-Center) as input and outputs the total amount of interfaces, the shutdown interfaces and the percental value of the shutdown interfaces. Furthermore, it prints the hostnames and the reachability status of all switches since a switch that is not reachable is treated as a switch on which all ports are shutdown.

Example Usage:
```python3 compute_interfaces_percentage.py --site=Dusseldorf
Switches found in Dusseldorf:

Switch: C9300-Lab
Status: Reachable
===========================
Location: Dusseldorf
Interfaces total: 46
Interfaces down: 42
91.3% of all interfaces down
```

### get_devices_and_print_info.py

Use Case: 
Our customer was interested in receiving the serial numbers of all devices of the inventory with a single click. This script simply polls all devices from Cisco DNA-Center and prints hostname, platform, management IP and serial number.

Example Usage: 
```python3 get_devices_and_print_info.py
C3650-Lab
WS-C3650-12X48FD-E
10.0.0.100
FDO2036V07E
```

### 
