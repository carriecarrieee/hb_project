from elasticsearch import Elasticsearch
import json
from pprint import pprint

def search_db(skill):
    esclient = Elasticsearch(['localhost:9200'])
    
    # title = "CHIEF OPERATING OFFICER"

    lon = 4.89994
    lat = 52.37815

    response = esclient.search(

    index='salaries',
    body={
        "query": {
            "bool": {
                "should": {
                    "multi_match": {
                        "query": skill,
                        "type": "best_fields",
                        "fields": ["TITLE", "SOC_NAME"]
                        }}
                "filter": {
                    "geo_distance": {
                        "distance": "10mi",
                            "location": [lon, lat]
                            }
                        }      
                    }   
                }
            }
        )

    

    print json.dumps(response, indent=4)
    pprint(response)

def get_locations():

    loc_list = []
    loc_dict = {}

    search_db(skill)
    results = response["hits"]["hits"]
    for result in results:
        loc_dict["lat"] = float(result["_source"]["lat"])
        loc_dict["lng"] = float(result["_source"]["lon"])
        loc_list.append(loc_dict)

    print loc_list

search_db("grape")
# https://www.elastic.co/guide/en/elasticsearch/reference/5.4/query-dsl-geo-distance-query.html
