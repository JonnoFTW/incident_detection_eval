from datetime import datetime

import argparse
from pymongo import MongoClient
from mongo_uri import mongo_uri
client = MongoClient(mongo_uri)
db = client['mack0242']
start = datetime(2012, 1, 1, 0, 0, 0)
end = datetime(2015, 12, 12, 23, 59)
drange = {'$gte': start, '$lte': end}


def get_location(intersection):
    return db['locations'].find_one({'site_no': intersection})


def get_data(intersection, ds):
    if ds == 'sm':
        return db['scats_sm'].find({'site_no': intersection, 'datetime': drange}).sort({'sequence:1'})
    elif ds == 'vs':
        return db['scats_readings'].find({'site_no': intersection, 'datetime': drange}).sort('datetime')


def run(data, location, method,si, ds):
    if method == 'htm':
        from htm_model import run_model
        run_model(db['scats_anomalies'], data, location, si, ds)
    elif method == 's-h-esd':
        from shesd import run_model
    else:
        from sesd import run_model


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('method')
    parser.add_argument('intersection')
    parser.add_argument('dataset', choices=['sm', 'vs'])
    parser.add_argument('si',)
    args = parser.parse_args()
    location = get_location(args.intersection)
    data = get_data(args.intersection, args.dataset)

    run(data, location, args.method,args.si, args.dataset)
