def make_row(row, location, ds, si):
    """

    :param row: the  row of data either vs or sm
    :param location: a location object
    :param ds: the datasource, either sm or vs
    :param si: the strategic input
    :return: a dict with keys 'datetime' and 'measured_flow'
    """
    si_confs = location['strategic_inputs']
    datestr = row['datetime'].strftime('%Y%m%d')

    si_conf = next(s for s in si_confs[::-1] if s['date'] <= datestr)
    to_process = {'datetime': row['datetime']}
    if ds == 'vs':
        to_process['measured_flow'] = sum(
            row['readings'][str(i)] for i in si_conf['si'][si]['sensors'] if row['readings'][str(i)] < 200)
    else:
        to_process['measured_flow'] = row['measured_flow']
    return to_process
