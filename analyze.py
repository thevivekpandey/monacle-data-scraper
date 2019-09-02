import json
from mo_mongo import MoMongo
from datetime import datetime
from datetime import timedelta
from datetime import date
from anomaly_calculator import AnomalyCalculator
from database import Database

def check_for_anomalies(grouped_data, tz, ref_date):
    #tz is not used currently
    anomalies = []
    for dim_val, time_series in grouped_data.items():
        ac = AnomalyCalculator(time_series, ref_date, dim_val)
        anomalies.extend(ac.check_anomalies())
    return anomalies

'''Output is like this:
    {
     'machine-1': {ts1: val1, ts2: val2...}
     'machine-2': {ts1: val1, ts2: val2...}
    }
'''
def group_by_dimension(data, dimension):
    grouped_data = {}
    for datum in data:
        dim_val = datum[dimension]
        grouped_data.setdefault(dim_val, {})
        ts = datum['ts']
        metric_val = datum['metricVal']
        grouped_data[dim_val][ts] = metric_val
    return grouped_data

if __name__ == '__main__':
    mo_mongo = MoMongo()
    database = Database()
    anomalies = []
    with open('rules.json') as f:
        rules = json.loads(f.read())['rules']
        for rule in rules:
            namespace = rule['namespace']
            dimension = rule['dimension']
            metric_name = rule['metricName']
            period = rule['period']
            function = rule['function_name']
        start_time = datetime.now() - timedelta(seconds=period + 86400)
        data = mo_mongo.get_data_from_mongo(namespace, dimension, metric_name, start_time)
        grouped_data = group_by_dimension(data, 'dimVal')
        anomalies.extend(check_for_anomalies(grouped_data, 'Asia/Taipei', date.today() - timedelta(1)))
    jsonified_anomalies = [anomaly.jsonify() for anomaly in anomalies]
    print('before')
    database.clear_anomalies(1)
    print('after')
    print(jsonified_anomalies)
    for anomaly in jsonified_anomalies:
        database.write_anomaly(1, anomaly)
