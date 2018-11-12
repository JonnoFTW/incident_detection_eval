from anomaly_detection import anomaly_detect_ts


def run_model(coll, ds, ts, location, data, count):
    results = anomaly_detect_ts(data,
                                max_anoms=0.02,
                                direction='both',
                                median_deviation=True,
                                only_last='day',
                                plot=False)
