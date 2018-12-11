from datetime import datetime, timedelta
import os
from anomaly_detection import anomaly_detect_vec
import pandas as pd
from util import make_row
import numpy as np


def run_model(coll, ds, location, si, data, count):
    period = 288
    lim = period * 10
    cache_fname = "/tmp/{}-{}-{}.pkl".format(location['site_no'], si, ds)
    if os.path.exists(cache_fname):
        print("loading cached pickle")
        series = pd.read_pickle(cache_fname)
    else:
        def make_ts(cursor):
            i = 0
            for row in cursor:
                out = make_row(row, location, ds, si)
                yield out

        df = pd.DataFrame(make_ts(data))
        df.set_index('datetime', inplace=True)
        series = pd.Series(df.measured_flow, index=df.index)
        if ds == 'vs':
            series = series.reindex(pd.date_range(series.index.min(), series.index.max(), freq='5min'),
                                    fill_value=np.nan)
        # fill in NaN values with interpolated values
        print("Filling")
        for k in series[series.isnull()].index:
            series[k] = series.loc[(series.index.weekday == k.weekday()) & (series.index.hour == k.hour) & (
                    series.index.minute == k.minute)].dropna().sample(1)
        print("Pickling series")
        series.to_pickle(cache_fname)
    print("finding anomalies")
    if ds == 'sm':
        sdate = datetime(2012, 3, 1)
        period = coll.database['scats_sm_small'].find({
            "site_no": location['site_no'],
            "strategic_input": int(si),
            "datetime": {
                "$gte": sdate,
                "$lte": sdate + timedelta(days=7)
            }
        }).count()
    results = anomaly_detect_vec(series.head(50000),
                                 alpha=0.05,
                                 direction='both',
                                 # longterm_period=period * 7,
                                 period=period,
                                 resampling=ds == 'sm',
                                 e_value=True
                                 )
    expected = results['expected']
    anoms = results['anoms']

    for k, anom in anoms.items():
        other = {'anom': anom, 'expected': None}
        try:
            other['expected'] = expected[k]
        except:
            pass
        doc = ({'site_no': location['site_no'],
                'strategic_input': si,
                'algorithm': 'shesd',
                'datetime': pd.to_datetime(k),
                'ds': ds,
                'other': other})
        coll.insert_one(doc)
