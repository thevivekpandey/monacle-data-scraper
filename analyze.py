import json
from mo_mongo import MoMongo
from datetime import datetime
from datetime import timedelta
from datetime import date
from anomaly_calculator import AnomalyCalculator

def check_for_anomalies(grouped_data, tz, ref_date):
    #tz is not used currently
    anomalies = []
    print('Checking unusually high cpu')
    for dim_val, time_series in grouped_data.items():
        ac = AnomalyCalculator(time_series, ref_date)
        anomaly = ac.check_unusually_high_cpu()
        if anomaly:
            anomalies.append(anomaly)
            print(dim_val, end=' ')
    print('Checking unusually low cpu')
    for dim_val, time_series in grouped_data.items():
        ac = AnomalyCalculator(time_series, ref_date)
        anomaly = ac.check_unusually_low_cpu()
        if anomaly:
            anomalies.append(anomaly)
            print(dim_val, end=' ')
    return anomalies

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
        #print(grouped_data)
        anomalies = check_for_anomalies(grouped_data, 'Asia/Taipei', date.today() - timedelta(1))

