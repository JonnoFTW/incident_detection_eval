from anomaly_detection import anomaly_detect_vec
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

    df = pd.DataFrame(make_ts(data))
    df.set_index('datetime', inplace=True)
    series = pd.Series(df.measured_flow, index=df.index)
    series = series.reindex(pd.date_range(series.index.min(), series.index.max(), freq='5min'), fill_value=np.nan)
    # fill in NaN values with interpolated values
    print("Filling")
    for k in series[series.isnull()].index:
        series[k] = series.loc[(series.index.weekday == k.weekday()) & (series.index.hour == k.hour) & (
                series.index.minute == k.minute)].dropna().sample(1)
    print("finding anomalies")
    results, all_anoms, seasonal_plus_trend = anomaly_detect_vec(series,
                                                                 alpha=0.05,
                                                                 direction='both',
                                                                 # longterm_period=period * 7,
                                                                 period=period)
    # series.plot()
    #
    # plt.scatter(results.index, results, c='r', zorder=100)
    # plt.show()
    for k, v in results.items():
        doc = ({'site_no': location['site_no'],
                'strategic_input': si,
                'algorithm': 'shesd',
                'datetime': pd.to_datetime(k),
                'ds': ds,
                'other': {}})
        coll.insert_one(doc)
