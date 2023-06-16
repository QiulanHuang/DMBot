# Get data from ES and do simple pre-process
# Written by Qiulan Huang  05/04/2023
import csv
from elasticsearch import Elasticsearch
# https://pypi.org/project/elasticsearch/
es = Elasticsearch(hosts="http://gs-elk02.sdcc.bnl.gov:9200/")
query_json = {
  "query": {
    "range": {
      "@timestamp": {
       "gte": "2023-04-28T00:00:00",
       "lt":  "2023-04-29T00:00:00",
       "time_zone": "America/New_York"
      }
    }
  }
}
query = es.search(index='dcache-billing-usatlas*',body=query_json,scroll='5m',size=100)
results = query['hits']['hits']
total = query['hits']['total']
print(total['value'])
scroll_id = query['_scroll_id']
with open('/lusatlasfs/LDRD/filterdata-0428.csv','w',newline='',encoding='utf-8') as flow:
     csv_writer = csv.writer(flow)

     for i in range(0, int(total['value']/100)+1):
       # scroll query
       query_scroll = es.scroll(scroll_id=scroll_id,scroll='5m')['hits']['hits']
       #results += query_scroll
       item = query_scroll
       #print(item)
       #csv_writer.writerow(res)
       for res in item:
         if (type(res['_source']['dcache']['billing']['protocol']['path']).__name__=='list'):
           #print(res['_source']['dcache']['billing']['protocol']['path'][0])
           csv_writer.writerow([res['_source']['@timestamp']+','+res['_source']['event']['action']+','+res['_source']['dcache']['billing']['protocol']['path'][0]+','+res['_source']['message']])
         else:
           #print(res['_source']['dcache']['billing']['protocol']['path'])
           csv_writer.writerow([res['_source']['@timestamp']+','+res['_source']['event']['action']+','+res['_source']['dcache']['billing']['protocol']['path']+','+res['_source']['message']])


print('done!')
print(es.info())
