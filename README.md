# PoC Cisco DNA-C Scripts
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
