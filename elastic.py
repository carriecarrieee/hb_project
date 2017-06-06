from elasticsearch import Elasticsearch
import json
from pprint import pprint

def search_db(term):
    esclient = Elasticsearch(['localhost:9200'])
 
    response = esclient.search(
 
        index='salaries',
        body={
            "query": {
                "bool": {
                    "should": {
                        "multi_match": {
                            "query": term,
                            "type": "best_fields",
                            "fields": [ "SOC_NAME", "TITLE" ]
                            }
                        }
                    }
                }
            }
        )

    # print json.dumps(response, indent=4)
    # pprint(response)
    return response

# search_db("executive")



# https://www.elastic.co/guide/en/elasticsearch/reference/5.4/query-dsl-geo-distance-query.html
