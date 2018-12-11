from __future__ import print_function
from main import drange
from generate_jobs import tss
from pymongo import MongoClient
from mongo_uri import mongo_uri
from datetime import timedelta
from matplotlib import pyplot as plt

client = MongoClient(mongo_uri)
incidents_coll = client['mack0242']['crashes']
locations_coll = client['mack0242']['locations']
anomalies_coll = client['mack0242']['scats_anomalies']
distance_to_crash = 100
site_nos = [t[0] for t in tss]
locations = list(locations_coll.find({'site_no': {'$in': site_nos}}, {'scats_diagram': 0}))
# all those crashes in the test period near the selected intersections
loc_dict = {x['site_no']: x for x in locations}
drange['$gte'] += timedelta(days=30)
all_crashes = []
for l in locations:
    c = list(incidents_coll.find({
        'datetime': drange,
        'loc': {'$near': {
            '$geometry': l['loc'],
            '$maxDistance': distance_to_crash
        }}
    }))
    for cr in c:
        cr['site_no'] = l['site_no']
    all_crashes.extend(c)

vs_all_readings = client['mack0242']['scats_readings'].find({
    'datetime': drange, 'site_no': {'$in': site_nos}
}).count()
sm_all_readings = client['mack0242']['scats_sm_small'].find({
    'datetime': drange, 'site_no': {'$in': site_nos}
}).count()

print("Total crashes    :", len(all_crashes))
print("Total VS readings:", vs_all_readings)
print("Total SM readings:", sm_all_readings)

all_readings = {
    'sm': sm_all_readings,
    'vs': vs_all_readings
}
dts = ['vs', 'sm']
# the task is to identify readings were correctly identified as anomalous AND had a crash nearby
located_crashes = {
    alg: {ds: {'fp': [], 'tp': []} for ds in dts} for alg in ['HTM', 'shesd', 'shesd-ts']
}
for method in 'HTM', 'shesd', 'shesd-ts':
    print(method)

    for ds in dts:
        confusion_matrix = {
            'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0
        }
        anomaly_count = 0
        for anomaly in anomalies_coll.find({'algorithm': method, 'datetime': drange, 'ds': ds}):
            anomaly_count += 1
            # find if there was a crash near this anomaly
            tr = {'$gte': anomaly['datetime'] - timedelta(minutes=10),
                  '$lte': anomaly['datetime'] + timedelta(minutes=10)}
            crashes = list(incidents_coll.find({
                'datetime': tr,
                'loc': {
                    '$near': {
                        '$geometry': loc_dict[anomaly['site_no']]['loc'],
                        '$maxDistance': distance_to_crash
                    }
                }
            }))
            for c in crashes:
                c['site_no'] = anomaly['site_no']
            if crashes:
                confusion_matrix['tp'] += len(crashes)
                located_crashes[method][ds]['tp'].extend(crashes)
            else:
                confusion_matrix['fp'] += 1
                located_crashes[method][ds]['fp'].extend(crashes)

        confusion_matrix['fn'] = len(all_crashes) - confusion_matrix['tp']
        confusion_matrix['tn'] = all_readings[ds] - confusion_matrix['fp']
        print("  Total Anomaly:", anomaly_count)
        print("\t", ds)
        for k, v in confusion_matrix.items():
            print("\t\t", k, v)
