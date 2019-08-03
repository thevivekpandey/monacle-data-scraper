import json
from mo_mongo import MoMongo
from datetime import datetime
from datetime import timedelta
from datetime import date
#from evaluator import high_cpu_util_yesterday

def check_for_single_anomaly(time_series, ref_date):
    sums_counts = {}
    for t, val in time_series.items():
        d = t.date()
        sums_counts.setdefault(d, {'sum': 0, 'count': 0})
        sums_counts[d]['sum'] += val
        sums_counts[d]['count'] += 1
    averages = {}
    for d, detail in sums_counts.items():
        averages[d] = detail['sum'] / detail['count']
    print(averages)

def check_for_anomalies(grouped_data, tz, ref_date):
    for dim_val, time_series in grouped_data.items():
        if dim_val == 'i-0fedbd54d59c494be':
            print("min:", min(time_series.keys()))
            print("max:", max(time_series.keys()))
            print("len:", len(time_series))
    #tz is not used currently
    anomalies = []
    for dim_val, time_series in grouped_data.items():
        if dim_val == 'i-0fedbd54d59c494be':
            anomaly = check_for_single_anomaly(time_series, ref_date)
            if anomaly:
                anomalies.append(anomaly)
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
        anomalies = check_for_anomalies(grouped_data, 'Asia/Taipei', date.today())
        print(anomalies)

