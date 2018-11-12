from datetime import datetime

import argparse
from pymongo import MongoClient
import pymongo.errors
from mongo_uri import mongo_uri

client = MongoClient(mongo_uri)
db = client['mack0242']
start = datetime(2012, 1, 1, 0, 0, 0)
end = datetime(2015, 12, 12, 23, 59)
drange = {'$gte': start, '$lte': end}


def get_location(intersection):
    return db['locations'].find_one({'site_no': intersection})


def cursor_gen(get_cursor):
    processed = 0
    while True:
        print("Loading cursor")
        c = get_cursor(processed)
        try:
            for row in c:
                yield row
                processed += 1
            c.close()
            break
        except pymongo.errors.CursorNotFound as e:
            pass


def get_data(intersection, ds):
    if ds == 'sm':
        def get_cursor(skip):
            return db['scats_sm'].find({
                'site_no': intersection,
                'datetime': drange},
                no_cursor_timeout=True).sort(
                [('sequence', 1)]).skip(skip)
    else:
        def get_cursor(skip):
            return db['scats_readings'].find({
                'site_no': intersection,
                'datetime': drange},
                no_cursor_timeout=True).sort(
                'datetime').skip(skip)
    c = get_cursor(0)
    count = c.count()
    c.close()
    return count, cursor_gen(get_cursor)


def run(data, location, method, si, ds, count):
    coll = db['scats_anomalies']
    if method == 'htm':
        from htm_model import run_model
        run_model(coll, data, location, si, ds, count)
    elif method == 's-h-esd':
        from shesd import run_model
        run_model(coll, ds, location, si, data, count)
    else:
        from sesd import run_model
        run_model(coll, ds, location, si, data, count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('method')
    parser.add_argument('intersection')
    parser.add_argument('dataset', choices=['sm', 'vs'])
    parser.add_argument('si', )
    args = parser.parse_args()
    location = get_location(args.intersection)
    count, data = get_data(args.intersection, args.dataset)

    run(data, location, args.method, args.si, args.dataset, count)
