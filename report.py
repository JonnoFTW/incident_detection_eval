from __future__ import print_function
from main import drange
from generate_jobs import tss
from pymongo import MongoClient
from mongo_uri import mongo_uri
from datetime import timedelta

client = MongoClient(mongo_uri)
incidents_coll = client['mack0242']['crashes']
locations_coll = client['mack0242']['locations']
anomalies_coll = client['mack0242']['scats_anomalies']

site_nos = [t[0] for t in tss]
locations = list(locations_coll.find({'site_no': {'$in': site_nos}}))
# all those crashes in the test period near the selected intersections

all_crashes = []
for l in locations:
    all_crashes.extend(incidents_coll.find({
        'datetime': drange,
        'loc': {'$near': {
            '$geometry': l['loc'],
            '$maxDistance': 200
        }}
    }))

vs_all_readings = client['mack0242']['scats_readings'].find({
    'datetime': drange, 'site_no': {'$in': site_nos}
}).count()

print("Total crashes    :", len(all_crashes))
print("Total VS readings:", vs_all_readings)

dts = ['vs']
# the task is to identify readings were correctly identified as anamalous AND had a crash nearby
for method in 'HTM', 'shesd':
    print(method)
    confusion_matrix = {
        m: {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0} for m in dts
    }
    for anomaly in anomalies_coll.find({'algorithm': method}):
        # find if there was a crash near this anomaly
        tr = {'$gte': anomaly['datetime'] - timedelta(minutes=5),
              '$lte': anomaly['datetime'] + timedelta(minutes=5)}
        crashes = incidents_coll.find({
            # 'loc':,
            'datetime': tr
        }).count()
        if crashes:
            confusion_matrix[anomaly['ds']]['tp'] += 1
        else:
            confusion_matrix[anomaly['ds']]['fp'] += 1

    print(confusion_matrix)
