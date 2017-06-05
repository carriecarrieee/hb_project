from elasticsearch import Elasticsearch
import json
from pprint import pprint

def search_db(search_term):
    esclient = Elasticsearch(['localhost:9200'])
 
    response = esclient.search(
 
        index='salaries',
        body={
            "query": {
                "bool": {
                    "should": {
                        "match": {
                            "TITLE": search_term,
                            }
                        }
                    }
                }
            }
        )

    # print json.dumps(response, indent=4)
    pprint(response)
    return response




# https://www.elastic.co/guide/en/elasticsearch/reference/5.4/query-dsl-geo-distance-query.html
