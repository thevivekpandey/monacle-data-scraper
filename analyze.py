import json
from mo_mongo import MoMongo
#from evaluator import high_cpu_util_yesterday

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
        data = mo_mongo.get_data_from_mongo(namespace, dimension, metric_name)
        grouped_data = group_by_dimension(data, 'dimVal')
        print(grouped_data)

