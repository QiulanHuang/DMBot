# Get raw data from ES
# Written by Qiulan Huang  05/03/2023
import csv
import sys
from elasticsearch import Elasticsearch


# Get input parameters

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python getESrawdata.py <start_date> <end_date> <output_file>")
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    output_file = sys.argv[3]


# Connect to ES and set up query

# https://pypi.org/project/elasticsearch/
es = Elasticsearch(hosts="http://gs-elk02.sdcc.bnl.gov:9200/")
query_json = {
    "query": {
        "range": {
            "@timestamp": {
                "gte": start_date,
                "lt": end_date,
                "time_zone": "America/New_York",
            }
        }
    }
}
query = es.search(
    index="dcache-billing-usatlas*", body=query_json, scroll="5m", size=100
)

# Parse the results and write to csv file

results = query["hits"]["hits"]
total = query["hits"]["total"]
print(total["value"])
scroll_id = query["_scroll_id"]
with open(output_file, "w", newline="", encoding="utf-8") as flow:
    csv_writer = csv.writer(flow)

    for i in range(0, int(total["value"] / 100) + 1):
        # scroll query
        query_scroll = es.scroll(scroll_id=scroll_id, scroll="5m")["hits"]["hits"]
        # results += query_scroll
        item = query_scroll
        # print(item)
        csv_writer.writerow(item)


print("done!")
print(es.info())
