"""Seeds the salaries database into elasticsearch."""


from elasticsearch import helpers, Elasticsearch
import csv


esclient = Elasticsearch(['localhost:9200'])

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'utf-8'):unicode(value, 'utf-8') for key, value in row.iteritems()}


with open('data/h1b_salaries.csv') as file:
    reader = UnicodeDictReader(file)
    helpers.bulk(esclient, reader, index='salaries', doc_type='h1b_apps')
