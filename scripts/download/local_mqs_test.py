# purpose
#   testing the metadata query service locally
# dependencies: 
#   `conda install -c conda-forge pystac-client`

from pystac_client import Client
from typing import Any, Dict
import json

mqs = Client.open("https://mqs.eodc.eu/stac/v1")

# search for collections
#for collection in mqs.get_all_collections():
#    print(collection)

# search for files within a collection
search_results = mqs.search(
    collections=[   #"sentinel1-grd",
                    #"urn:eop:VITO:CGS_S1_GRD_L1"
                    "urn:eop:VITO:TERRASCOPE_S5P_L3_NO2_TD_V1"
                ],
    bbox=[9.5,46.0,48.5,49.5],
    #datetime=['2022-01-01T00:00:00Z', '2022-06-01T00:00:00Z'],
    max_items=20
    )

# search for files within a collection using intersect
# coordinates given as first longitude then latitude
polygon_dict: Dict[str,Any] = {
    "type": "Polygon",
    "coordinates": [
      [
        [
            133.41796874999997,
            40.713955826286046
        ],
        [
            144.31640625,
            33.137551192346145
        ],
        [
            146.77734375,
            41.244772343082076
        ],
        [
            130.95703125,
            46.800059446787316
        ],
        [
            133.41796874999997,
            40.713955826286046
        ]
      ]
    ]    
}


search_results = mqs.search(
    collections=[   #"sentinel1-grd",
                    #"urn:eop:VITO:CGS_S1_GRD_L1"
                    "urn:eop:VITO:TERRASCOPE_S5P_L3_NO2_TD_V1"
                ],
    intersects=polygon_dict,
    #datetime=['2022-01-01T00:00:00Z', '2022-06-01T00:00:00Z'],
    max_items=20
    )


for item in search_results.items():
    print(item.id)
