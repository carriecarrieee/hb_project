from elasticsearch import Elasticsearch
import json
from pprint import pprint

def query_h1bdb(title):
    esclient = Elasticsearch(['localhost:9200'])
    
    title = "CHIEF OPERATING OFFICER"

    lon = 4.89994
    lat = 52.37815
    response = esclient.search(


    index='salaries',
    body={
        "query": {
            "bool": {
                "should": {
                    "match": {
                        "TITLE": title
                        }},
                "must": {    
                    "geo_shape": {
                        "location": { 
                            "shape": { 
                                "type": "circle", 
                                "radius": "1km",
                                "coordinates": [lon, lat]
                                }
                            }
                        }
                    }}
                }
            }
        )

    

    print json.dumps(response, indent=4)
    pprint(response)

    # loc_list = []
    # loc_dict = {}

    # results = response["hits"]["hits"]
    # for result in results:
    #     loc_dict["lat"] = float(result["_source"]["lat"])
    #     loc_dict["lng"] = float(result["_source"]["lon"])
    #     loc_list.append(loc_dict)

    # print loc_list

query_h1bdb("grape")

