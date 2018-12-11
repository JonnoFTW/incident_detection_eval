from anomaly_detection import anomaly_detect_ts
import pandas as pd
from util import make_row
import numpy as np


def run_model(coll, ds, location, si, data, count):
    period = 288
    lim = period * 10

    def make_ts(cursor):
        i = 0
        for row in cursor:
            out = make_row(row, location, ds, si)

            yield out
            # i += 1
            # if i > lim:
            #     return

    df = pd.DataFrame(make_ts(data))
    df.set_index('datetime', inplace=True)
    series = pd.Series(df.measured_flow, index=df.index)
    if ds == 'vs':
        series = series.reindex(pd.date_range(series.index.min(), series.index.max(), freq='5min'), fill_value=np.nan)
    print("Series Size:", series.memory_usage())
    # fill in NaN values with interpolated values
    print("Filling")
    for k in series[series.isnull()].index:
        series[k] = series.loc[(series.index.weekday == k.weekday()) & (series.index.hour == k.hour) & (
                series.index.minute == k.minute)].dropna().sample(1)
    print("Finding anomalies")
    results = anomaly_detect_ts(series,
                                alpha=0.05,
                                direction='both',
                                e_value=True,
                                longterm=True,
                                piecewise_median_period_weeks=8,
                                resampling=ds == 'sm',
                                multithreaded=True)
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
                'algorithm': 'shesd-ts',
                'datetime': pd.to_datetime(k),
                'ds': ds,
                'other': other})
        # print(doc)
        coll.insert_one(doc)
