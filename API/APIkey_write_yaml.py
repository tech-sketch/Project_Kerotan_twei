# APIkey_write_yaml.py

import yaml
import os
import sys

# make data of API key.
data = {}
data.update({
    "Bing search API": {
        "url": "https://api.datamarket.azure.com/Bing/Search/Web?",
        "key": "" 	# INPUT YOUR LICENSE KEY.
        }
    })
data.update({
    "Ekitan API": {
        "url": "http://go.ekitan.com/asp-servlet/TrialAPI?",
        "key": "", 	# INPUT YOUR LICENSE KEY.
        }
})
data.update({
    "Google Maps Geocoding API": {
        "url": "",
        "key": "", 	# INPUT YOUR LICENSE KEY.
        }
    })

# write data
try:
    with open(os.path.dirname(os.path.abspath(__file__))+u"/API_KEY.yaml","w") as f:
        f.write(yaml.dump(data))
except:
    print('write yaml error.')
    raise